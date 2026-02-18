from abc import ABC, abstractmethod
from typing import Protocol
import numpy as np

class Engine(ABC):
    """
    Abstract engine class

    Engines will be one of:
    Black-Scholes,
    Monte Carlo,
    Binomial Tree
    """

    @abstractmethod
    def calculate_price(self, instrument, market_state, stochastic_model=None):
        pass

class MonteCarloEngine(Engine):
    def __init__(
            self,
            num_simulations=100_000,
            antithetic=True,
            control_variate=True,
            random_seed=None,
            bump_size=0.01,
            n_steps=252
        ):
            self.num_simulations = num_simulations
            self.antithetic = antithetic
            self.control_variate = control_variate
            self.rng = np.random.default_rng(random_seed)
            self.bump_size = bump_size
            self.effective_simulations = num_simulations // 2 if self.antithetic else self.num_simulations
        

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