
from .base import StochasticModel

class GBM(StochasticModel):
    """
    Reference: https://www.gregorygundersen.com/blog/2024/04/13/simulating-gbm/
    """
    def __init__(self, seed=None):
        self.seed = seed # the seed

    def generate_expectation(self, S, T, r, sigma):
        return S * np.exp(r * T)


    def generate_paths(self, S, T, r, sigma, n_paths, n_steps):
        if self.seed is not None:
            np.random.seed(self.seed)
        
        dt = T / n_steps

        m = (r - 0.5 * sigma**2)

        log_returns = np.random.normal(
            m * dt,
            sigma * np.sqrt(dt),
            size=(n_steps, n_paths))
        
        cumulative_log_returns = np.cumsum(log_returns, axis=0)

        initial_log_price = np.zeros((1, n_paths))
        full_log_path = np.vstack([initial_log_price, cumulative_log_returns])

        return S * np.exp(full_log_path)
