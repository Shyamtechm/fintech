from data_loader import load_data
from portfolio_analysis import analyze_portfolio
from risk_analysis import analyze_risk
from option_pricing import price_put_option
from hedging_engine import hedge_decision

prices = load_data()
stats = analyze_portfolio(prices)
returns = analyze_risk(prices)

vol = stats.stats.loc['daily_vol'].values[0]
decision = hedge_decision(vol)

price, delta = price_put_option()

print("\nOption Price:", price)
print("Option Delta:", delta)
print("Hedging Decision:", decision)
