from .base import Instrument
from ..engine.base import Engine

class Equity(Instrument):
    """
    Class for the stock instrument
    """
    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker # stock symbol
    
    def payoff(self, market_state):
        return market_state.S

    class EquityEngine(Engine):
        def calculate_price(self, instrument, market_state):
            return market_state.S

        def delta(self, instrument, market_state):
            DELTA = 1.0
            return DELTA
    
        def gamma(self, instrument, market_state):
            GAMMA = 0.0
            return GAMMA
        
        def vega(self, instrument, market_state):
            VEGA = 0.0
            return VEGA
        
        def theta(self, instrument, market_state):
            THETA = 0.0
            return THETA
        
        def rho(self, instrument, market_state):
            RHO = 0.0
            return RHO

