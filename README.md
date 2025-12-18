This project replicates and optimises the "Time Series Momentum" (Moskowitz, Ooi, Pedersen, 2012) as a risk hedge in the post-2020 inflationary macro regime.


The basic model used a 12-month lookback design providing diversification; however, this engine implements a Multi-Frequency Signal Bleeding strategy to reduce whipsaw variance. This strategy generated a significant amount of Crisis Alpha during the 2022 inflationary bear market, delivering positive returns, whereas the S&P500, used as a control in this research, suffered double digit losses.


1.	KEY FINDINGS:
  
   Sharpe Ratio: 0.96 
   
   Beta: -0.08
  
  Statistical Significance: t = 4.61
2.	Strategy Methodology: The logic of the engine moves beyond the typical "buy and hold" strategy. Multi-frequency signal bleeding allows for dynamic adjustment of exposure to assets based on trend and volatility. Instead of a 12-month "lookback" signal, the algorithm blends three-time horizons together to create a continuous "conviction score".


Fast Trend: 1 Month, captures immediate breakouts 

Medium Trend: 3 Months, filters noise

Slow Trend: 12 Months. captures the macro cycle.


The basic description of the mechanism is that leverage is reduced during market chaos and increased in calm periods.


The basic model using the 12-month lookback method had a vol target of 0.15 (15%) in order to account for the Sharpe ratio of 0.91. However, as the more robust, optimised model has a Sharpe ratio of 0.96, it can allow for a higher target vol. Therefore, a volatility of 0.2 (20%) was chosen, to increase potential alpha.


3.	Performance Analysis: The chart below compares the Optimised Blended Strategy (Green) against the Basic Model (Blue) and the S&P500 benchmark (Grey).
<img width="1270" height="706" alt="Tradingalgoblended" src="https://github.com/user-attachments/assets/4eb55072-dca0-470a-aad5-2d6039b4a1b8" />

During 2022, traditional portfolios failed due to stock/bond correlation spiking to 1.0. However this strategy successfully identifies the downtrend in equities and uptrend in commodities/USD, generating positive returns when liquidity was needed most.

4.	Statistical variation: To ensure results were not random or luck, an Ordinary Least Squares regression was conducted against the S&P500. 


--- FINAL STATS --- 

Annualized Alpha: 11.50% - Pure excess return after risk adjustment 

Beta to S&P 500: -0.08 - Strategy is market neutral, but slightly inverse 

Alpha t-statistic: 4.61 Statistically significant (>2.0) 

P-Value: 0.00000 <0.01% probability of random chance


5.	Repository structure:

momentum_engine.py: Core logic
  
regression_analysis.py: Econometric verification using statsmodels
  
Tradingalgoblended.png: Visual output

   
6.	Installation and Usage:
A: Clone repository Bash git clone https://github.com/yourusername/Time-Series-Momentum.git
B: Install dependencies bash pip install yfinance pandas numpy matplotlib statsmodels
C: Run the engine bash python momentum_engine.py







THIS ANALYSIS WAS CONDUCTED AS AN INDEPENDANT QUANTITATIVE ANALYSIS RESEARCH PROJECT BY GEORGE COBURN, B.COM/B.ECON STUDENT, UNIVERSITY OF QUEENSLAND
