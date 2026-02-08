from ..data.loader import DataFetcher
from ..data.processor import MarketProcessor
from ..data.state import MarketState
from ..instruments.option import EuropeanOption, CALL, PUT

prices = DataFetcher.get_historical_data("AAPL", "2023-01-01", "2024-01-01")
raw_r = DataFetcher.get_risk_free_rate()

processor = MarketProcessor(prices)
spot = processor.get_spot_price()
vol = processor.get_realized_volatility()

r = raw_r / 100 # BAD

market = MarketState(ticker="AAPL", S=spot, sigma=vol, r=r)

strike = market.S
expiry = 0.5
option = EuropeanOption(K=strike, T=expiry, option_type=CALL)

engine = option.BlackScholes()
price = engine.calculate_price(option, market)
greeks = engine.calculate_greeks(option, market)

print(f"price: {price}")
print(f"greeks: {greeks}")