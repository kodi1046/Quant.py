from abc import ABC, abstractmethod
from typing import Protocol

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

class Greeks(Protocol):
    def delta(self, instrument, market_state):
        ...
    def gamma(self, instrument, market_state):
        ...
    def vega(self, instrument, market_state):
        ...
    def theta(self, instrument, market_state):
        ...
    def rho(self, instrument, market_state):
        ...