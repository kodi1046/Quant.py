import numpy as np
from .base import StochasticModel
from ..data.state import MarketState

class JumpDiffusion(StochasticModel):
    """
    Jump Diffusion stochastic model.
    
    The implementation is based on the following reference material.
    Reference: https://www.codearmo.com/python-tutorial/merton-jump-diffusion-model-python
    
    Attributes
    ----------
    lmbda: int
        The average number of jumps per annum.
    mu: float
        The expected log-jump size.
    delta: float
        The standard deviation of the log-jump size.
    """
    def __init__(self, lmbda, mu, delta):
        self.lmbda = lmbda 
        self.mu = mu 
        self.delta = delta 

    def generate_expectation(self, market_state: MarketState):
        """
        Calculate the expectation of the underlying asset at the given market_state.

        The expectation is calculated as:
            S * exp(r * T)

        Parameters
        ----------
        market_state: MarketState
            The market state at which to calculate the expectation.
        
        Returns
        -------
        float
            The expectation of the asset.
        """
        S = market_state.S
        r = market_state.r
        T = market_state.T
        return S * np.exp(r * T)

    def generate_paths(self, market_state: MarketState, n_paths: int, n_steps: int):
        """
        Generates Jump Diffusion paths.

        The formula for Jump Diffusion is calculated as:
            S_t+delta_t = S_t(1 + mu * delta_t + sigma * delta_t^0.5 * Z) * J^k
        Where delta_t = T / n_steps, and Z is sampled from the random distribution N(0,1), and J is a random jump multiplier. 

        Parameters
        ----------
        market_state: MarketState
            The market state at which to generate paths.
        n_paths: int
            The number of paths to generate.
        n_steps: int
            The number of steps each path takes.

        Returns
        -------
        np.vstack
            A matrix containing the spot price at each step for n_paths many paths.
        """
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
