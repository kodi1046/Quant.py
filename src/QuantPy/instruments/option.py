import numpy as np
from .base import Instrument
from ..engine.base import Engine

CALL = 'call'
PUT = 'put'

class VanillaOption(Instrument):
    def __init__(self, K, T, option_type):
        super().__init__()
        self.K = K # strike price
        self.T = T # expiry
        if option_type not in [CALL, PUT]:
            raise ValueError(f"Invalid option_type: {option_type}")
        self.option_type = option_type
    
    def payoff(self, S_T):
        if self.option_type == CALL:
            return np.maximum(S_T - self.K, 0)
        return np.maximum(self.K - S_T, 0)
        
class EuropeanOption(VanillaOption):
    class BlackScholes(Engine):
        pass
    class MonteCarlo(Engine):
        """
        The Monte Carlo engine for a European option
        """
        def __init__(self, n_paths=10000, seed=42):
            self.n_paths = n_paths # number of paths
            self.seed = seed # the seed
        
        def calculate_price(self, instrument, market_state):
            pass

        def calculate_greeks(self, instrument, market_state):
            pass


class AmericanOption(VanillaOption):
    pass

class ExoticOption(Instrument):
    pass