import numpy as np
from scipy.stats import norm
from .base import Instrument, Greeks
from ..engine.base import Engine, Greeks
from ..data.state import MarketState

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
    
    class MonteCarlo(Engine):
        """
        The Monte Carlo engine for vanilla options
        """
        def __init__(
            self,
            num_simulations=100_000,
            antithetic=True,
            control_variate=True,
            random_seed=None,
            bump_size=0.01
        ):
            self.num_simulations = num_simulations
            self.antithetic = antithetic
            self.control_variate = control_variate
            self.rng = np.random.default_rng(random_seed)
            self.bump_size = bump_size

            self.effective_simulations = num_simulations // 2 if self.antithetic else self.num_simulations
        
        def _simulate_terminal_prices(self, S, r, sigma, T):
            """
            Generate terminal stock prices under risk-neutral measure
            """
            Z = self.rng.standard_normal(self.effective_simulations)

            if self.antithetic:
                Z = np.concatenate([Z, -Z])
            
            drift = (r - 0.5 * sigma**2) * T
            diffusion = sigma * np.sqrt(T) * Z

            S_T = S * np.exp(drift + diffusion)
            return S_T
        
        def calculate_price(self, instrument, market_state):
            S = market_state.S
            K = instrument.K
            T = market_state.T
            r = market_state.r
            sigma = market_state.sigma
            q = market_state.q

            drift = (r - q - 0.5 * sigma**2) * T

            S_T = self._simulate_terminal_prices(S, r - q, sigma, T)

            payoffs = np.array([instrument.payoff(s_t) for s_t in S_T
            ])

            price = np.exp(-r * T) * np.mean(payoffs)

            return price
        
        def delta(self, instrument, market_state):
            h_s = self.bump_size * market_state.S
            up_state = MarketState(
                market_state.ticker, 
                market_state.S + h_s, 
                market_state.series, 
                market_state.sigma, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            down_state = MarketState(
                market_state.ticker, 
                market_state.S - h_s, 
                market_state.series, 
                market_state.sigma, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            price_up = self.calculate_price(instrument, up_state)
            price_down = self.calculate_price(instrument, down_state)
            return (price_up - price_down) / (2 * h_s)
        
        def gamma(self, instrument, market_state):
            h_s = self.bump_size * market_state.S
            up_state = MarketState(
                market_state.ticker, 
                market_state.S + h_s, 
                market_state.series, 
                market_state.sigma, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            down_state = MarketState(
                market_state.ticker, 
                market_state.S - h_s, 
                market_state.series, 
                market_state.sigma, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            
            delta_up = (self.calculate_price(instrument, up_state) - price_base) / h_s
            delta_down = (price_base - self.calculate_price(instrument, down_state)) / h_s

            return (delta_up - delta_down) / (2 * h_s)
        
        def vega(self, instrument, market_state):
            h_v = self.bump_size * market_state.sigma
            vega_up_state = MarketState(
                market_state.ticker, 
                market_state.S, 
                market_state.series, 
                market_state.sigma + h_v, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            vega_down_state = MarketState(
                market_state.ticker, 
                market_state.S, 
                market_state.series, 
                market_state.sigma - h_v, 
                market_state.r, 
                market_state.q, 
                market_state.T)
            price_v_up = self.calculate_price(instrument, vega_up_state)
            price_v_down = self.calculate_price(instrument, vega_down_state)

            return (price_v_up - price_v_down) / (2 * h_v)
        
        def theta(self, instrument, market_state):
            h_t = self.bump_size * market_state.T 
            theta_down_state = MarketState(
                market_state.ticker, 
                market_state.S, 
                market_state.series, 
                market_state.sigma, 
                market_state.r, 
                market_state.q, 
                market_state.T - h_t)
            price_theta_down = self.calculate_price(instrument, theta_down_state)
            return - (price_theta_down - price_base) / h_t
        
        def rho(self, instrument, market_state):
            h_r = self.bump_size 
            rho_up_state = MarketState(
                market_state.ticker, 
                market_state.S, 
                market_state.series, 
                market_state.sigma, 
                market_state.r + h_r, 
                market_state.q, 
                market_state.T)
            rho_down_state = MarketState(
                market_state.ticker, 
                market_state.S, 
                market_state.series, 
                market_state.sigma, 
                market_state.r - h_r, 
                market_state.q, 
                market_state.T)
            price_r_up = self.calculate_price(instrument, rho_up_state)
            price_r_down = self.calculate_price(instrument, rho_down_state)
            return (price_r_up - price_r_down) / (2 * h_r)
        
class EuropeanOption(VanillaOption):
    class BlackScholes(Engine):
        """
        The Black Scholes engine for a European option
        """
        @staticmethod
        def _d1(instrument, market_state):
            return (np.log(market_state.S / instrument.K) 
                + (market_state.r +  0.5 * market_state.sigma**2) 
                * market_state.T) / (market_state.sigma * np.sqrt(market_state.T))
        
        @staticmethod 
        def _d2(instrument, market_state):
            return BlackScholes._d1(instrument, market_state) - instrument.sigma * np.sqrt(market_state.T)

        def calculate_price(self, instrument, market_state):
            r, S, sigma = market_state.r, market_state.S, market_state.sigma
            K, T = instrument.K, instrument.T

            phi = 1 if instrument.option_type == CALL else -1
            
            if T <= 0:
                return instrument.payoff(S)

            d1 = BlackScholes._d1(instrument, market_state)
            d2 = BlackScholes._d2(instrument, market_state)

            return phi * (S * norm.cdf(phi * d1) - K * np.exp(-r * T) * norm.cdf(phi * d2))

        
        
        def delta(self, instrument, market_state):
            return norm.cdf(BlackScholes._d1(instrument, market_state)) if instrument.option_type == CALL else norm.cdf(BlackScholes._d1(instrument, market_state)) - 1

        def gamma(self, instrument, market_state):
            return norm.pdf(BlackScholes._d1(instrument, market_state)) / (market_state.S * market_state.sigma * np.sqrt(market_state.T))
        
        def vega(self, instrument, market_state):
            return market_state.S * np.sqrt(market_state.T) * norm.pdf(BlackScholes._d1(instrument, market_state))
        
        def theta(self, instrument, market_state):
            phi = 1 if instrument.option_type == CALL else -1
            theta_term1 = -(market_state.S * norm.pdf(BlackScholes._d1(instrument, market_state)) * market_state.sigma) / (2 * np.sqrt(market_state.T))
            theta_term2 = phi * market_state.T * instrument.K * np.exp(-market_state.r * market_state.T) * norm.cdf(phi * BlackScholes._d2(instrument, market_state))
            return theta_term1 - theta_term2

        def rho(self, instrument, market_state):
            phi = 1 if instrument.option_type == CALL else -1
            return phi * market_state.T * instrument.K * np.exp(-market_state.r * market_state.T) * norm.cdf(phi * BlackScholes._d2(instrument, market_state))

class AmericanOption(VanillaOption):
    class BinomialTree(Engine):
        """
        The Binomial Tree engine for an American option
        """
        def calculate_price(self, instrument, market_state):
            pass


class ExoticOption(Option):
    pass

