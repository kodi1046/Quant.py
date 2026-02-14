from .portfolio import Portfolio, Position
from ..data.state import MarketState
from .order import Order, OrderSide
from ..instruments.option import Option
from ..instruments.equity import Equity

class Backtest:
    def __init__(self, ticker, price_series, r, sigma):
        self.ticker = ticker
        self.price_series = price_series
        self.r = r
        self.sigma = sigma
        self.portfolio = None
    
    def run(self, strategy, engine):
        self.portfolio = Portfolio(initial_cash=10000)
        for date, price in self.price_series[self.ticker].items():
            start_date = min(self.price_series[self.ticker].keys())
            days_passed = (date - start_date).days
            T_remaining = max(strategy.instrument.T - days_passed / 365.25, 0.0001)
            market_state = MarketState(ticker=self.ticker, S=price, series=self.price_series, sigma=self.sigma, r=self.r, T=T_remaining)

            self.portfolio.mark_to_market(market_state=market_state, engine=engine)

            trades = strategy.on_data(date, market_state, self.portfolio)

            for order in trades:
                unit_price = order.instrument.price(market_state)

                existing_pos = None
                for p in self.portfolio.positions:
                    if p.instrument is order.instrument:
                        existing_pos = p
                        break
                
                signed_qty = order.quantity if order.side == OrderSide.BUY else -order.quantity

                if existing_pos:
                    existing_pos.quantity += signed_qty
                    if existing_pos.quantity != 0:
                        old_val = existing_pos.entry_price * (existing_pos.quantity - signed_qty)
                        new_val = unit_price * signed_qty
                        existing_pos.entry_price = (old_val + new_val) / existing_pos.quantity
                    else:
                        self.portfolio.positions.remove(existing_pos)
                else:
                    pos = Position(order.instrument, signed_qty, unit_price)
                    self.portfolio.add_position(pos)
                
                self.portfolio.cash -= signed_qty * unit_price
            
            self.portfolio.cleanup_expired(market_state, date)
        
            self.portfolio.record_snapshot(date, market_state, engine)


