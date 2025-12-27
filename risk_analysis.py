import pyfolio as pf

def analyze_risk(prices):
    returns = prices.to_returns().dropna()
    pf.create_full_tear_sheet(returns)
    return returns
