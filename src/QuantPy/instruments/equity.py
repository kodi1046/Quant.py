from .base import Instrument

class Equity(Instrument):
    """
    Class for the stock instrument
    """
    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker # stock symbol
    
    def payoff(self, S_t):
        return S_t
