import numpy as np
from scipy.stats import norm
from .base import Instrument
from ..engine.base import Engine

CALL = 'call'
PUT = 'put'

class Option(Instrument):
    pass
class VanillaOption(Option):
    def __init__(self, K, T, option_type, expiry=None):
        super().__init__()
        self.K = K # strike price
        self.T = T # expiry
        if option_type not in [CALL, PUT]:
            raise ValueError(f"Invalid option_type: {option_type}")
        self.option_type = option_type
        self.expiry = expiry
    
    def payoff(self, S):
        if self.option_type == CALL:
            return np.maximum(S - self.K, 0)
        return np.maximum(self.K - S, 0)
        
class EuropeanOption(VanillaOption):
    class BlackScholes(Engine):
        """
        The Black Scholes engine for a European option
        """
        def calculate_price(self, instrument, market_state):
            r, S, sigma = market_state.r, market_state.S, market_state.sigma
            K, T = instrument.K, instrument.T

            phi = 1 if instrument.option_type == CALL else -1
            
            if T <= 0:
                return instrument.payoff(S)

            d1 = (np.log(S / K) + (r +  0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            return phi * (S * norm.cdf(phi * d1) - K * np.exp(-r * T) * norm.cdf(phi * d2))

        def calculate_greeks(self, instrument, market_state):
            r, S, sigma = market_state.r, market_state.S, market_state.sigma
            K, T = instrument.K, market_state.T

            if T <= 0:
                return instrument.payoff(market_state.S)

            phi = 1 if instrument.option_type == CALL else -1

            d1 = (np.log(S / K) + (r +  0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            pdf_d1 = norm.pdf(d1)
            df = np.exp(-r * T)
            sqrt_T = np.sqrt(T)

            delta = norm.cdf(d1) + (phi - 1) / 2
            gamma = pdf_d1 / (S * sigma * sqrt_T)
            vega = S * sqrt_T * pdf_d1
            rho = phi * T * K * df * norm.cdf(phi * d2)

            theta_term1 = -(S * pdf_d1 * sigma) / (2 * sqrt_T)
            theta_term2 = phi * r * K * df * norm.cdf(phi * d2)
            theta = theta_term1 - theta_term2

            return {
                "delta": delta,
                "gamma": gamma,
                "vega": vega,
                "theta": theta,
                "rho": rho
            }

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
    class BinomialTree(Engine):
        """
        The Binomial Tree engine for an American option
        """
        def calculate_price(self, instrument, market_state):
            pass
        def calculate_greeks(self, instrument, market_state):
            pass


class ExoticOption(Option):
    pass

