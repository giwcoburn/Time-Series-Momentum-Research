import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- STEP 1: SETUP & DOWNLOAD ---
tickers = {
    'Equities_US': 'SPY', 'Equities_EAFE': 'EFA', 
    'Bonds_10Y': 'IEF', 'Bonds_20Y': 'TLT',
    'Commodities': 'DBC', 'Gold': 'GLD',
    'Real_Estate': 'VNQ', 'Bitcoin': 'BTC-USD'
}
VOL_WINDOW = 60

print("Downloading Data... (Please wait)")
df_prices = yf.download(list(tickers.values()), start="2010-01-01", end="2025-12-01")['Close']

if isinstance(df_prices.columns, pd.MultiIndex):
    df_prices.columns = df_prices.columns.get_level_values(0)
inv_tickers = {v: k for k, v in tickers.items()}
df_prices = df_prices.rename(columns=inv_tickers)
daily_rets = df_prices.pct_change()

# --- STEP 2: CALCULATE SIGNALS ---
# Strategy A: Basic (12-Month only)
trend_basic = np.sign(df_prices - df_prices.shift(252))

# Strategy B: Blended (1M + 3M + 12M)
sig_fast = np.sign(df_prices - df_prices.shift(21))
sig_med  = np.sign(df_prices - df_prices.shift(63))
sig_slow = np.sign(df_prices - df_prices.shift(252))
trend_blended = (sig_fast + sig_med + sig_slow) / 3.0

# --- STEP 3: VOLATILITY SCALING ---
rolling_vol = daily_rets.rolling(window=VOL_WINDOW).std() * np.sqrt(252)

# BASIC Strategy: Target 15% Vol due to a lower sharpe ratio
vol_scalar_basic = 0.15 / rolling_vol
vol_scalar_basic = vol_scalar_basic.clip(upper=2.0)

# BLENDED Strategy: Target 20% Vol due to a higher sharpe ratio
vol_scalar_blended = 0.20 / rolling_vol
vol_scalar_blended = vol_scalar_blended.clip(upper=2.5)

# Apply positions
pos_basic = (trend_basic * vol_scalar_basic).shift(1)
pos_blended = (trend_blended * vol_scalar_blended).shift(1)

# --- STEP 4: CALCULATE RESULTS ---
rets_basic = (pos_basic * daily_rets).mean(axis=1)
rets_blended = (pos_blended * daily_rets).mean(axis=1)
rets_spy = daily_rets['Equities_US']

cum_basic = (1 + rets_basic).cumprod()
cum_blended = (1 + rets_blended).cumprod()
cum_spy = (1 + rets_spy).cumprod()

# Calculate Stats for the Legend
ann_ret_basic = rets_basic.mean() * 252
ann_ret_blended = rets_blended.mean() * 252
ann_ret_spy = rets_spy.mean() * 252

sharpe_basic = rets_basic.mean() / rets_basic.std() * np.sqrt(252)
sharpe_blended = rets_blended.mean() / rets_blended.std() * np.sqrt(252)
sharpe_spy = rets_spy.mean() / rets_spy.std() * np.sqrt(252)

# --- STEP 5: THE CHART ---
plt.figure(figsize=(12, 7))

# Plot Benchmark (Grey)
cum_spy.plot(label=f'S&P 500 | Ret: {ann_ret_spy:.1%} | Sharpe: {sharpe_spy:.2f}', 
             color='grey', alpha=0.3, linewidth=1.5, linestyle='--')

# Plot Basic (Blue)
cum_basic.plot(label=f'Basic (12M) | Ret: {ann_ret_basic:.1%} | Sharpe: {sharpe_basic:.2f}', 
               color='tab:blue', alpha=0.6, linewidth=1.5)

# Plot Blended (Green)
cum_blended.plot(label=f'Blended (1M/3M/12M) | Ret: {ann_ret_blended:.1%} | Sharpe: {sharpe_blended:.2f}', 
                 color='tab:green', linewidth=3.0)

plt.title("Optimization Effect: Signal Blending vs. Basic Momentum (2010-2025)")
plt.ylabel("Growth of $1 Investment")

plt.legend(loc="lower right", fontsize=10, frameon=True, facecolor='white', framealpha=0.9)

plt.grid(True, alpha=0.2)
plt.show()

print(f"S&P 500 Sharpe:  {sharpe_spy:.2f}")
print(f"Basic Sharpe:    {sharpe_basic:.2f}")
print(f"Blended Sharpe:  {sharpe_blended:.2f}")
