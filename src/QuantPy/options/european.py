from api import Option

class EuropeanCallOption(Option):
    def __init__(self):
        super().__init__()

    def payoff(self, maturity_price):
        return np.maximum(maturity_price - self.strike, 0)