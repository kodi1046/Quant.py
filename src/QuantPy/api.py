from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Dict, Tuple

class Option(ABC):
    """Abstract class for all options."""

    def __init__(
        self, 
        initial_value: float,
        strike: float,
        time_horizon: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0
    ):
        self.initial_value = initial_value
        self.strike = strike
        self.time_horizon = time_horizon
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.dividend_yield = dividend_yield
    
    @abstractmethod
    def payoff(self, t):
        pass


class StochasticProcess(ABC):
    """abstract class for all stochastics."""

    def __init__(
        self,
        drift: float,
        volatility: float,
        initial_value: float,
        correlation: np.matrix.__float__,
        seed = None,

    ):
        self.drift = drift
        self.volatility = volatility
        self.initial_value = initial_value
        self.correlation = correlation
        self.seed = seed

    @abstractmethod
    def generate_paths(num_paths: int, num_steps: int, T: float):
        pass

class Simulation(ABC):
    """abstract class for all simulations."""

    def __init__(
        option: Option,
        process: StochasticProcess,
        num_paths: int,
        num_steps: int
    ):
        self.option = option
        self.process = process
        self.num_paths = num_paths
        self.num_steps = num_steps

    @abstractmethod 
    def run(self):
        pass