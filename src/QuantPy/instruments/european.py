import numpy as np

from ..api import Option

class EuropeanCallOption(Option):
    def payoff(self, ST):
        return np.maximum(ST - self.K, 0)