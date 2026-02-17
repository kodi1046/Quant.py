from abc import ABC, abstractmethod

from ..instruments.equity import Equity
from .order import Order, OrderSide

class Strategy(ABC):
    def __init__(self, params=None):
        self.params = params or {}

    @abstractmethod
    def on_data(self, date, market_state, portfolio):
        pass

class DeltaHedgeStrategy(Strategy):
    def __init__(self, instrument, quantity, engine, params=None):
        super().__init__(params)
        self.instrument = instrument
        self.target_qty = quantity
        self.engine = engine
        self.initialized = False
        self.equity_instrument = None
        self.threshold = 1.0

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
                self.equity_instrument = Equity(market_state.ticker)
                self.equity_instrument.set_engine(self.equity_instrument.EquityEngine())
            
            trades.append(Order(
                hedge_side,
                self.equity_instrument,
                abs_hedge_qty
            ))
        
        return trades
