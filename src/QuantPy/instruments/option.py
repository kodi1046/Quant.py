import numpy as np
from scipy.stats import norm
from .base import Instrument, Greeks
from ..engine.base import Engine, Greeks, MonteCarloEngine
from ..data.state import MarketState

CALL = 'call'
PUT = 'put'

class Option(Instrument):
    def __init__(self, K, T, option_type, expiry=None):
        super().__init__()
        self.K = K # strike price
        self.T = T # expiry
        if option_type not in [CALL, PUT]:
            raise ValueError(f"Invalid option_type: {option_type}")
        self.option_type = option_type
        self.expiry = expiry
class VanillaOption(Option):
    def payoff(self, market_state):
        if self.option_type == CALL:
            return np.maximum(market_state.S - self.K, 0)
        return np.maximum(self.K - market_state.S, 0)
    
    class MonteCarlo(MonteCarloEngine):
        """
        The Monte Carlo engine for vanilla options
        """
        
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

            payoffs = []

            for s_t in S_T:
                temp_state = MarketState(
                    ticker=market_state.ticker,
                    S=s_t,                     
                    series=market_state.series,  
                    sigma=market_state.sigma,
                    r=market_state.r,
                    q=market_state.q,
                    T=0.0                      
                )
                payoffs.append(instrument.payoff(temp_state))

            payoffs = np.array(payoffs)
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
                return instrument.payoff(market_state)

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
    """
    Base for all exotic options
    """
    pass

class AsianOption(ExoticOption):
    def __init__(
        self, 
        K, 
        T, 
        option_type, 
        averaging_type="arithmetic", 
        expiry=None):
        super().__init__(self, K, T, option_type, expiry)
        ARITHMETIC_TYPE = "arithmetic"
        GEOMETRIC_TYPE = "geometric"
        if averaging_type not in [ARITHMETIC_TYPE, GEOMETRIC_TYPE]:
            raise ValueError(f"Invalid averaging_type: {averaging_type}")
        self.averaging_type = averaging_type
    
    def payoff(self, market_state):
        if market_state.path is None:
            raise ValueError("Path-dependent option requires market_state.path to be set")
        
        path = market_state.path
        avg = np.mean(path)
        return max(avg - self.K, 0) if self.option_type == CALL else max(self.K - avg, 0)
       

    class MonteCarlo(MonteCarloEngine):
        """
        Path-dependent MonteCarlo engine for Asian option
        """
        def calculate_price(self, instrument, market_state, stochastic_model):
            """
            Prices Asian options using full path simulation from given model.
            """
            if stochastic_model is None:
                raise ValueError("Path-dependent options need a stochastic_model to be specified.")

            S = market_state.S
            r = market_state.r
            q = market_state.q
            sigma = market_state.sigma
            T = market_state.T
            
            if T <= 0:
                temp_state = MarketState(
                    ticker=market_state.ticker, 
                    S=S,
                    series=market_state.series,
                    sigma=sigma,
                    r=r,
                    q=q,
                    T=0.0)
                return instrument.payoff(temp_state)
            
            paths = stochastic_model.generate_paths(
                S=S,
                T=T,
                r=r - q,
                sigma=sigma,
                n_paths=self.effective_simulations,
                n_steps=self.n_steps)
            
            payoffs = []
            for path in paths:
                temp_state = MarketState(
                    ticker=market_state.ticker,
                    S=path[-1],
                    series=market_state.series,
                    sigma=sigma,
                    r=r,
                    q=q,
                    T=0.0,
                    path=path
                )
                payoffs.append(instrument.payoff(temp_state))
            
            payoffs = np.array(payoffs)
            price = np.exp(-r * T) * np.mean(payoffs)
            return price

