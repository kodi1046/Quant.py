from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Dict, Tuple

class Option(ABC):
    """Abstract class for all options."""

    def __init__(
        self, 
        initial_value: float,
        strike: float,
        T: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0
    ):
        self.initial_value = initial_value
        self.strike = strike
        self.T = T
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
        S0: float, # initial value
        sigma: float, # volatility 
        mu: float, # drift
    ):
        self.S0 = S0
        self.sigma = sigma
        self.mu = mu


    @abstractmethod
    def generate_paths(self, num_paths: int, num_steps: int, T: float):
        pass

class Simulation(ABC):
    """abstract class for all simulations."""

    def __init__(
        option: Option,
        process: StochasticProcess,
        r: float,

    ):
        self.option = option
        self.process = process
        self.r = r

    @abstractmethod 
    def run(self, num_paths, num_steps):
        pass