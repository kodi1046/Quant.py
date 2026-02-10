from abc import ABC, abstractmethod

from ..instruments.equity import Equity

class Strategy(ABC):
    def __init__(self, params=None):
        self.params = params or {}

    @abstractmethod
    def on_data(self, date, market_state, portfolio):
        pass

# example
class DeltaHedgeStrategy(Strategy):
    def __init__(self, instrument, quantity, engine, params=None):
        super().__init__(params)
        self.instrument = instrument
        self.target_qty = quantity
        self.engine = engine
        self.initialized = False

    def on_data(self, date, market_state, portfolio):
        trades = []

        if not self.initialized:
            trades.append(('BUY', self.instrument, self.target_qty))
            self.initialized = True
            return trades
        
        current_greeks = portfolio.get_greeks(market_state, self.engine)
        net_delta = current_greeks['delta']

        threshold = self.params.get('threshold', 0.01)

        if abs(net_delta) > threshold:
            hedge_qty = -net_delta
            equity_instrument = Equity(market_state.ticker)
            trades.append(('BUY', equity_instrument, hedge_qty))
        
        return trades
