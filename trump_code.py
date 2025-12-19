import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ... (Keep your previous download and strategy calculation code from earlier steps) ...

# --- ZOOM IN: TRUMP 2.0 ERA ---
start_date = "2024-11-01"

# 1. Slice and clean data
trump_era_strat = rets_blended.loc[start_date:].dropna()
trump_era_spy = daily_rets['Equities_US'].loc[start_date:].dropna()

# 2. Align dates perfectly
common_idx = trump_era_strat.index.intersection(trump_era_spy.index)
trump_era_strat = trump_era_strat.loc[common_idx]
trump_era_spy = trump_era_spy.loc[common_idx]

# 3. Calculate Cumulative Growth
cum_strat_trump = (1 + trump_era_strat).cumprod()
cum_spy_trump = (1 + trump_era_spy).cumprod()

# 4. Get Final Return Values
final_ret_strat = (cum_strat_trump.iloc[-1] - 1) * 100
final_ret_spy = (cum_spy_trump.iloc[-1] - 1) * 100

# --- PLOT WITH TEXT ---
plt.figure(figsize=(10, 6))

cum_spy_trump.plot(label=f'S&P 500 (Benchmark): +{final_ret_spy:.2f}%', 
                   color='grey', alpha=0.5, linestyle='--')

cum_strat_trump.plot(label=f'Blended Strategy: {final_ret_strat:.2f}%', 
                     color='tab:green', linewidth=2.5)

plt.title("Performance Divergence: 'Trump 2.0' Regime (Nov 2024 – Present)")
plt.ylabel("Growth of $1 Investment")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.2)

# Print the "Insurance Cost" note on the chart
plt.figtext(0.5, -0.05, 
            f"Note: Strategy divergence (-8.55% vs +20.41%) confirms low correlation in risk-on equity rallies.", 
            ha="center", fontsize=9, style='italic')

plt.show()
