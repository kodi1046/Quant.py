from abc import ABC, abstractmethod
import numpy as np
from ..data.state import MarketState
from ..engine.base import Engine

class Instrument(ABC):
    """
    Abstract Instrument class.

    Attributes
    ----------
        engine: Engine
            The engine that should be used to calculate the price of the instrument.
            Default is None
    """
    def __init__(self):
        self.engine = None
    
    def set_engine(self, engine: Engine):
        """
        Sets the engine of the instrument.

        Parameters
        ----------
        engine: Engine
            The engine to use.
        """
        self.engine = engine
    
    def _check_engine(self):
        if self.engine is None:
            raise ValueError("No pricing engine found, don't forget to set it")
    
    def price(self, market_state: MarketState):
        self._check_engine()
        return self.engine.calculate_price(self, market_state)
    
    def delta(self, market_state: MarketState):
        self._check_engine()
        return self.engine.delta(self, market_state)
    
    def gamma(self, market_state: MarketState):
        self._check_engine()
        return self.engine.delta(self, market_state)
    
    def vega(self, market_state: MarketState):
        self._check_engine()
        return self.engine.vega(self, market_state)
    
    def theta(self, market_state: MarketState):
        self._check_engine()
        return self.engine.vega(self, market_state)
    
    def rho(self, market_state: MarketState):
        self._check_engine()
        return self.engine.rho(self, market_state)

    @abstractmethod
    def payoff(self, market_state: MarketState):
        pass

