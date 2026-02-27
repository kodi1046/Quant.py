from abc import ABC, abstractmethod
from typing import Protocol
import numpy as np
from ..data.state import MarketState
from ..models.base import StochasticModel
from typing import TYPE_CHECKING

# Temporary way to avoid circular imports.
if TYPE_CHECKING:
    from .instrument import Instrument

class Engine(ABC):
    """
    Abstract engine class.
    """
    @abstractmethod
    def calculate_price(
        self, 
        instrument: "Instrument", 
        market_state: MarketState, 
        stochastic_model: StochasticModel=None):
        pass

class MonteCarloEngine(Engine):
    """
    Abstract class for Monte Carlo engines. Implemented for Vanilla and Exotic options.

    Attributes
    ----------
    num_simulations: int, optional
        The number of Monte Carlo simulations that should be done. Default is 100_000
    anthithetic: bool, optional
        If the Monte Carlo enine should be anthithetic,
        (meaning that you only generate half of the paths, and then mirror them about the x-axis).
        Default is True
    control_variate: bool, optional
        FIXME: clarify the usefullness of this.
        Default is True
    random_seed: int, optional
        The random seed to use for random number generation. Default is None
    bump_size: float, optional
        The bump-weight used for finite differences. Default is 0.01       
    n_steps: int, optional
        The number of steps in each path, (i.e. days). Default is 252 (1 business year)
    """
    def __init__(
            self,
            num_simulations: int=100_000,
            antithetic: bool=True,
            control_variate: bool=True,
            random_seed: int=None,
            bump_size: float=0.01,
            n_steps: int=252
        ):
            self.num_simulations = num_simulations
            self.antithetic = antithetic
            self.control_variate = control_variate
            self.rng = np.random.default_rng(random_seed)
            self.bump_size = bump_size
            self.effective_simulations = num_simulations // 2 if self.antithetic else self.num_simulations
            self.n_steps = n_steps
        

class Greeks(Protocol):
    """
    Protocol (interface) for the Greeks calculations. Implemented by Engine.
    """
    def delta(self, instrument: "Instrument", market_state: MarketState):
        ...
    def gamma(self, instrument: "Instrument", market_state: MarketState):
        ...
    def vega(self, instrument: "Instrument", market_state: MarketState):
        ...
    def theta(self, instrument: "Instrument", market_state: MarketState):
        ...
    def rho(self, instrument: "Instrument", market_state: MarketState):
        ...
