def analyze_portfolio(prices):
    stats = prices.calc_stats()
    print("\nPortfolio Performance:")
    stats.display()
    return stats
