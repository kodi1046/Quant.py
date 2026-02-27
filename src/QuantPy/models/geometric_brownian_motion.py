
from .base import StochasticModel
from ..data.state import MarketState

class GBM(StochasticModel):
    """
    Geometric Brownian Motion stochastic model.

    The implementation is based on the following reference material.
    Reference: https://www.gregorygundersen.com/blog/2024/04/13/simulating-gbm/

    Attributes
    ----------
    seed: int
        The seed to use for random number generation. Default is None.
    """
    def __init__(self, seed=None):
        self.seed = seed

    def generate_expectation(self, market_state: MarketState):
        """
        Calculates the expected value of the underlying asset at the given market_state.

        The expectation is calculated as:
            S * exp(r * T)

        FIXME: Should just take a market state

        Parameters
        ----------
        market_state: MarketState
            The market state to use to generate the expectation.

        Returns
        -------
        float
            The expectation of the asset.
        """
        S = market_state.S 
        r = market_state.r 
        T = market_state.T 
        return S * np.exp(r * T)


    def generate_paths(
            self, 
            market_state: MarketState, 
            n_paths: int, 
            n_steps: int):
        """
        Generates paths of brownian motion.

        The formula for the GBM is the Euler-Maruyama discretized formula:
            S_n+1 = S_n * exp((mu - 0.5 * sigma^2) * delta_t + sigma * delta_t^0.5 * Z_n)
        Where delta_t = T / n_steps, and Z_n is sampled from the normal distribution N(0,1). 

        Parameters
        ----------
        market_state: MarketState
            The market state at which to calculate the paths.
        n_paths: int
            The number of paths to generate.
        n_steps: int
            The number of steps that each GBM takes. 
        
        Returns
        -------
        np.vstack
            A matrix containing the spot price at each step for n_paths many paths.      
        """
        T = market_state.T 
        sigma = market_state.sigma 
        S = market_state.S

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
