from .base import Instrument
from ..engine.base import Engine

class Equity(Instrument):
    """
    Class for the stock instrument
    """
    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker # stock symbol
    
    def payoff(self, S):
        return S
    
    class EquityEngine(Engine):
        def calculate_price(self, instrument, market_state):
            return market_state.S

        def calculate_greeks(self, instrument, market_state):
            return {
                "delta": 1.0,
                "gamma": 0.0,
                "vega": 0.0,
                "theta": 0.0,
                "rho": 0.0
            }