
class Backtest:
    def __init__(self, ticker, price_series, r):
        self.ticker = ticker
        self.price_series = price_series
        self.r = r
    
    def run(self, strategy):
        pass