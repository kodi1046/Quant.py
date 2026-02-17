from abc import ABC, abstractmethod
import numpy as np
from ..engine.base import Engine, Greeks

class Instrument(ABC):
    def __init__(self):
        self.engine = None
    
    def set_engine(self, engine):
        self.engine = engine
    
    def _check_engine(self):
        if self.engine is None:
            raise ValueError("No pricing engine found, don't forget to set it")
    
    def price(self, market_state):
        self._check_engine()
        return self.engine.calculate_price(self, market_state)
    
    def delta(self, market_state):
        self._check_engine()
        return self.engine.delta(self, market_state)
    
    def gamma(self, market_state):
        self._check_engine()
        return self.engine.delta(self, market_state)
    
    def vega(self, market_state):
        self._check_engine()
        return self.engine.vega(self, market_state)
    
    def theta(self, market_state):
        self._check_engine()
        return self.engine.vega(self, market_state)
    
    def rho(self, market_state):
        self._check_engine()
        return self.engine.rho(self, market_state)

    @abstractmethod
    def payoff(self, market_state):
        pass

