from abc import ABC, abstractmethod

class StochasticModel(ABC):
    """
    Abstract class for stochastic models.
    """
    @abstractmethod
    def generate_expectation(self, S, T, r, sigma):
        pass
    
    @abstractmethod
    def generate_paths(self, S, T, r, sigma, n_paths, n_steps):
        pass

    
