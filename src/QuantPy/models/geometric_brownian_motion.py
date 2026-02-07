
from .base import StochasticModel

class GBM(StochasticModel):
    def __init__(self, seed=None):
        self.seed = seed # the seed
    
    def generate_expectation(self, S_T, T, r, sigma):
        pass

    def generate_paths(self, S_T, T, r, sigma, n_paths, n_steps):
        pass