import ffn

def load_data():
    symbols = 'AAPL,MSFT,TSLA,SPY'
    prices = ffn.get(symbols, start='2020-01-01')
    return prices
