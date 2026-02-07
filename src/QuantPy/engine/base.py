from abc import ABC, abstractmethod

class Engine(ABC):
    """
    Abstract engine class

    Engines will be one of:
    Black-Scholes,
    Monte Carlo,
    Binomial Tree
    """

    @abstractmethod
    def calculate_price(self, instrument, market_state):
        pass

    @abstractmethod
    def calculate_greeks(self, instrument, market_state):
        pass