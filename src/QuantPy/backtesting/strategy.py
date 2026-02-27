from abc import ABC, abstractmethod

from ..instruments.equity import Equity
from .order import Order, OrderSide

class Strategy(ABC):
    """
    The strategy class.

    Attributes
        params: Dict
            The parameters for the strategy (free to choose).
            Default is None.
    """
    def __init__(self, params=None):
        self.params = params or {}

    @abstractmethod
    def on_data(self, date, market_state, portfolio):
        pass

class DeltaHedgeStrategy(Strategy):
    """
    The Delta Hedge Strategy.

    Attributes
    ----------
    instrument: Instrument
        The instrument to use for hedging (preferrably an option).
    target_qty: int
        The quantity of options to start with.
    
    engine: Engine
        The engine to use to calculate the price of the instrument.
    """
    def __init__(self, instrument, quantity, engine, params=None):
        super().__init__(params)
        self.instrument = instrument
        self.target_qty = quantity
        self.engine = engine
        self.initialized = False
        self.equity_instrument = None
        self.threshold = 1.0
    
    """
    on_data is called once for every new data point (e.g. each trading day), 
    and looks at the current market state; 
    then it computes what strategy it wants to do (i.e. hedge if delts is too large), 
    and then it returns a list of trades/orders to execute.
    
    Parameters
    ----------
    date: datetime
        The current date.
    market_state: MarketState
        The current market state, associated to the date.
    portfolio: Portfolio
        The current portfolio, also related to the current state.

    Returns
    -------
    List:
        A list containing all Orders to be executed on the current time.
    """
    def on_data(self, date, market_state, portfolio):
        trades = []

        # initial trade
        if not self.initialized:
            side = OrderSide.BUY if self.target_qty > 0 else OrderSide.SELL
            trades.append(Order(side, self.instrument, abs(self.target_qty)))
            self.initialized = True
        
        net_delta = portfolio.get_delta(market_state, self.engine)
        threshold = self.params.get('threshold', self.threshold)

        if abs(net_delta) > threshold and abs(net_delta) > self.threshold:
            hedge_qty = -net_delta
            hedge_side = OrderSide.BUY if hedge_qty > 0 else OrderSide.SELL
            abs_hedge_qty = abs(hedge_qty)

            if self.equity_instrument is None:
                self.equity_instrument = Equity()
                self.equity_instrument.set_engine(self.equity_instrument.EquityEngine())
            
            trades.append(Order(
                hedge_side,
                self.equity_instrument,
                abs_hedge_qty
            ))
        
        return trades
