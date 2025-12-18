import statsmodels.api as sm

# --- STEP 6: RUN REGRESSION ON THE BLENDED MODEL ---

# 1. Align the data (Strategy vs. Market)
data_reg = pd.concat([rets_blended, daily_rets['Equities_US']], axis=1).dropna()
data_reg.columns = ['Blended_Strategy', 'Market']

# 2. Define Y (Strategy) and X (Market)
Y = data_reg['Blended_Strategy']
X = data_reg['Market']
X = sm.add_constant(X) # Adds the Alpha intercept

# 3. Run the Regression
model_blended = sm.OLS(Y, X).fit()

# 4. Print the Results
print(model_blended.summary())

# 5. Extract Key Metrics for your Post/CV
alpha_annual = model_blended.params['const'] * 252
beta = model_blended.params['Market']
t_stat = model_blended.tvalues['const']
p_val = model_blended.pvalues['const']

print("\n--- FINAL STATS ---")
print(f"Annualized Alpha: {alpha_annual:.2%}")
print(f"Beta to S&P 500:  {beta:.2f} (Should be near 0)")
print(f"Alpha t-statistic: {t_stat:.2f} (Should be > 2.0)")
print(f"P-Value: {p_val:.5f}")
