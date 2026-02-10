from .portfolio import Portfolio, Position
from ..data.state import MarketState

class Backtest:
    def __init__(self, ticker, price_series, r, sigma):
        self.ticker = ticker
        self.price_series = price_series
        self.r = r
        self.sigma = sigma
    
    def run(self, strategy, engine):
        portfolio = portfolio(initial_cash=10000)

        for date, price in self.price_series.items():
            market_state = MarketState(self.ticker, S=price, r=self.r, sigma=self.sigma)
            portfolio.mark_to_market(market_state, engine)
            trades = strategy.on_data(date, market_state, portfolio)

            portfolio.cleanup_expired(market_state)
            portfolio.record_snapshot(date, market_state, engine)

