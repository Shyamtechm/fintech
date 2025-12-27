def hedge_decision(volatility):
    if volatility > 0.20:
        return "High risk → Buy SPY Put Options"
    else:
        return "Low risk → No hedge needed"
