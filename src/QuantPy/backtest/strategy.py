from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, params=None):
        self.params = params or {}

    @abstractmethod
    def on_data(self, date, market_state, portfolio):
        pass

# example
class DeltaHedgeStrategy(Strategy):
    def on_data(self, date, market_state, portfolio):
        pass