from QuantPy.data.state import MarketState

from .base import Instrument
from ..engine.base import Engine

class Equity(Instrument):
    """
    Class for the stock instrument.
    """
    def payoff(self, market_state: MarketState):
        """
        Calculates the payoff of a stock.

        The payoff is just the current market price.

        Parameters
        ----------
        market_state: MarketState
            The market state with which to evaluate the payoff.
        
        Returns
        -------
        float
            The payoff of the stock at a given market state
        """
        return market_state.S

    class EquityEngine(Engine):
        def calculate_price(self, instrument: Instrument, market_state: MarketState):
            """
            Calculates the price of a stock at a given market state.

            The price of the stock is just the market price of the stock.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, but should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the price. 

            Returns
            -------
            float
                The price of the stock.
            """
            return market_state.S

        def delta(self, instrument: Instrument, market_state: MarketState):
            """
            Calculates the delta of the stock at a given market state.

            The delta of a stock is always 1.0.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the delta. 
                Is not used here, so should just be the current state, or None.
            
            Returns
            -------
            float
                The stock delta (1.0)
            """
            DELTA = 1.0
            return DELTA
    
        def gamma(self, instrument, market_state):
            """
            Calculates the gamma of the stock at a given market state.

            The gamma of a stock is always 0.0.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the delta. 
                Is not used here, so should just be the current state, or None.
            
            Returns
            -------
            float
                The stock gamma (0.0)
            """
            GAMMA = 0.0
            return GAMMA
        
        def vega(self, instrument, market_state):

            """
            Calculates the vega of the stock at a given market state.

            The vega of a stock is always 0.0.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the delta. 
                Is not used here, so should just be the current state, or None.
            
            Returns
            -------
            float
                The stock vega (0.0)
            """
            VEGA = 0.0
            return VEGA
        
        def theta(self, instrument, market_state):
            """
            Calculates the theta of the stock at a given market state.

            The theta of a stock is always 0.0.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the delta. 
                Is not used here, so should just be the current state, or None.
            
            Returns
            -------
            float
                The stock theta (0.0)
            """
            THETA = 0.0
            return THETA
        
        def rho(self, instrument, market_state):
            """
            Calculates the rho of the stock at a given market state.

            The rho of a stock is always 0.0.

            Parameters
            ----------
            instrument: Instrument
                Not needed for this calculation, should just be the equity instrument itself,
                or None.
            market_state: MarketState
                The market state with which to evaluate the delta. 
                Is not used here, so should just be the current state, or None.
            
            Returns
            -------
            float
                The stock rho (0.0)
            """
            RHO = 0.0
            return RHO

