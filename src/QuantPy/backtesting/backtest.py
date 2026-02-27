import pandas as pd

from .portfolio import Portfolio, Position
from ..data.state import MarketState
from .order import Order, OrderSide
from ..instruments.option import Option
from ..instruments.equity import Equity
from .strategy import Strategy
from ..engine.base import Engine

class Backtest:
    """
    Class for backtesting a strategy on a price series.

    Parameters
    ----------
    ticker: str
        The ticker for the underlying price series.
    price_series: pd.DataFrame
        The actual price series to use for backtesting.
    r: float
        The risk-free rate.
    sigma: float
        The volatiltiy of the asset.
    """
    def __init__(
        self, 
        ticker: str, 
        price_series: pd.DataFrame, 
        r: float,
        sigma: float):
        self.ticker = ticker
        self.price_series = price_series
        self.r = r
        self.sigma = sigma
        self.portfolio = None
    
    def run(self, strategy: Strategy, engine: Engine):
        """
        Runs a backtest with a given strategy and engine.

        Parameters
        ----------
        strategy: Strategy
            The strategy to backtest.
        engine: Engine
            The engine to use to calculate the price of the asset.
        Note
        ----
        - The default amount of initial_cash is $10000
        - The engine, the underlying asset, and the startegy all need to be compatible.
        """
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


