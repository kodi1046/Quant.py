from abc import ABC, abstractmethod
import numpy as np

class Option(ABC):
    """Abstract class for all options."""

    def __init__(
        self, 
        S0: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
    ):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
    
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
        self,
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