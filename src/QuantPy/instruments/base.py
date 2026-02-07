from abc import ABC, abstractmethod
import numpy as np

class Instrument(ABC):
    def __init__(self):
        self.engine = None
    
    def set_engine(self, engine):
        self.engine = engine
    
    def price(self, market_state):
        if self.engine is None:
            raise ValueError("No pricing engine found")
        return self.engine.calculate_price(self, market_state)

    @abstractmethod
    def payoff(self, market_state):
        pass
