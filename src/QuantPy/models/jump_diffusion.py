import numpy as np
from .base import StochasticModel

class JumpDiffusion(StochasticModel):
    """
    Reference: https://www.codearmo.com/python-tutorial/merton-jump-diffusion-model-python
    """

    def __init__(self, lmbda, mu, delta):
        self.lmbda = lmbda # average number of jumps per annum
        self.mu = mu # expected log-jump size
        self.delta = delta # std deviation of the log-jump size

    def generate_expectation(self, S, T, r, sigma):
        return S * np.exp(r * T)

    def generate_paths(self, S, T, r, sigma, n_paths, n_steps):
        dt = T / n_steps

        kappa = np.exp(self.mu + 0.5 * self.delta**2) - 1
        drift = (r -  0.5 * sigma**2 - self.lmbda * kappa) * dt

        shocks = np.random.normal(0, 1, (n_steps, n_paths))
        gbm_log_returns = drift + (sigma * np.sqrt(dt) * shocks)

        jump = np.random.poisson(self.lmbda * dt, (n_steps, n_paths))
        jump_sizes = np.random.normal(self.mu, self.delta, (n_steps, n_paths))
        jump_log_returns = jumps * jump_sizes

        total_log_returns = gbm_log_returns + jump_log_returns
        cumulative_log_returns = np.cumsum(total_log_returns, axis=0)

        starting_row = np.zeros((1, n_paths))
        full_log_path = np.vstack([starting_row, cumulative_log_returns])

        return S * np.exp(full_log_path)