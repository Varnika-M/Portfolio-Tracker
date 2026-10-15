"""Global Portfolio Tracker & Performance Dashboard.

Setup:  pip install streamlit yfinance pandas numpy plotly
Run:    streamlit run global_portfolio_app.py

Features: multi-currency holdings, FX conversion to a base currency,
region / asset class / currency allocation, risk metrics (volatility,
Sharpe, max drawdown), and benchmark comparison.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Global Portfolio Dashboard", layout="wide")
st.title("Global Portfolio Tracker & Performance Dashboard")

# ---------- Sidebar settings ----------
base = st.sidebar.selectbox("Base currency", ["USD", "INR", "EUR", "GBP", "JPY"])
period = st.sidebar.selectbox("History window", ["6mo", "1y", "2y", "5y"], index=1)
rf = st.sidebar.number_input("Risk-free rate (%)", value=4.0, step=0.25) / 100

BENCHMARKS = {  # name: (ticker, currency the benchmark is quoted in)
    "S&P 500 (SPY)": ("SPY", "USD"),
    "MSCI World (URTH)": ("URTH", "USD"),
    "Nifty 50 (^NSEI)": ("^NSEI", "INR"),
    "Nikkei 225 (^N225)": ("^N225", "JPY"),
    "Euro Stoxx 50 (^STOXX50E)": ("^STOXX50E", "EUR"),
}
bench_name = st.sidebar.selectbox("Benchmark", list(BENCHMARKS))

# ---------- Holdings input ----------
# Buy Price is in the asset's own (local) currency.
default = pd.DataFrame({
    "Ticker": ["AAPL", "ASML.AS", "7203.T", "RELIANCE.NS", "GLD"],
    "Shares": [10, 3, 50, 20, 8],
    "Buy Price": [150.0, 650.0, 2000.0, 2400.0, 180.0],
    "Currency": ["USD", "EUR", "JPY", "INR", "USD"],
    "Region": ["US", "Europe", "Japan", "India", "Global"],
    "Asset Class": ["Equity", "Equity", "Equity", "Equity", "Commodity"],
})
st.subheader("Holdings (edit, add or remove rows)")
holdings = st.data_editor(default, num_rows="dynamic", use_container_width=True)
holdings = holdings.dropna().reset_index(drop=True)


# ---------- Data helpers ----------
@st.cache_data(ttl=600)
def history(ticker: str, period: str) -> pd.Series:
    s = yf.Ticker(ticker).history(period=period)["Close"]
    s.index = s.index.tz_localize(None).normalize()  # align across exchanges
    return s


def to_base(series: pd.Series, cur: str) -> pd.Series:
    """Convert a price series from `cur` into the base currency."""
    if cur == base:
        return series
    fx = history(f"{cur}{base}=X", period)  # e.g. EURUSD=X = USD per 1 EUR
    fx = fx.reindex(series.index.union(fx.index)).ffill().reindex(series.index)
    return series * fx


if holdings.empty:
    st.stop()

# ---------- Build per-holding value history in base currency ----------
values, failed = {}, []
for _, r in holdings.iterrows():
    try:
        px_local = history(r["Ticker"], period)
        values[r["Ticker"]] = to_base(px_local, r["Currency"]) * r["Shares"]
    except Exception:
        failed.append(r["Ticker"])

if failed:
    st.warning(f"Could not load data for: {', '.join(failed)}. Check the ticker symbols.")
if not values:
    st.stop()

val_hist = pd.concat(values, axis=1).sort_index().ffill().dropna()
port = val_hist.sum(axis=1)

# ---------- Current positions table ----------
latest = val_hist.iloc[-1]
pos = holdings[holdings["Ticker"].isin(latest.index)].copy()
pos["Value"] = pos["Ticker"].map(latest)
# Cost basis converted at today's FX rate (simplification; note in README)
cost_local = pos["Shares"] * pos["Buy Price"]
cost_fx = pos["Currency"].apply(
    lambda c: 1.0 if c == base else float(history(f"{c}{base}=X", period).iloc[-1])
)
pos["Cost"] = cost_local * cost_fx
pos["P&L"] = pos["Value"] - pos["Cost"]
pos["Return %"] = pos["P&L"] / pos["Cost"] * 100
pos["Weight %"] = pos["Value"] / pos["Value"].sum() * 100

# ---------- Risk metrics ----------
daily = port.pct_change().dropna()
ann_vol = daily.std() * np.sqrt(252)
ann_ret = (port.iloc[-1] / port.iloc[0]) ** (252 / len(daily)) - 1
sharpe = (ann_ret - rf) / ann_vol if ann_vol else np.nan
drawdown = port / port.cummax() - 1

# ---------- Benchmark (converted to base currency, rebased to 100) ----------
b_ticker, b_cur = BENCHMARKS[bench_name]
bench = to_base(history(b_ticker, period), b_cur).reindex(port.index).ffill().dropna()
common = port.index.intersection(bench.index)
compare = pd.DataFrame({
    "Portfolio": port.loc[common] / port.loc[common].iloc[0] * 100,
    bench_name: bench.loc[common] / bench.loc[common].iloc[0] * 100,
})

# ---------- Dashboard ----------
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric(f"Value ({base})", f"{pos['Value'].sum():,.0f}")
m2.metric("Total P&L", f"{pos['P&L'].sum():,.0f}",
          f"{pos['P&L'].sum() / pos['Cost'].sum() * 100:.1f}%")
m3.metric("Ann. volatility", f"{ann_vol * 100:.1f}%")
m4.metric("Sharpe ratio", f"{sharpe:.2f}")
m5.metric("Max drawdown", f"{drawdown.min() * 100:.1f}%")

st.subheader("Portfolio vs benchmark (rebased to 100)")
st.line_chart(compare)

st.subheader("Allocation")
a1, a2, a3 = st.columns(3)
for col, key in zip((a1, a2, a3), ("Region", "Asset Class", "Currency")):
    grp = pos.groupby(key, as_index=False)["Value"].sum()
    col.plotly_chart(px.pie(grp, names=key, values="Value", title=f"By {key}"),
                     use_container_width=True)

st.subheader("Positions")
st.dataframe(pos.round(2), use_container_width=True)

st.subheader("Drawdown")
st.area_chart(drawdown * 100)

st.subheader("Correlation between holdings (daily returns)")
corr = val_hist.pct_change().dropna().corr()
st.plotly_chart(px.imshow(corr.round(2), text_auto=True, zmin=-1, zmax=1,
                          color_continuous_scale="RdBu_r"), use_container_width=True)
