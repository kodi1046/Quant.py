
class MarketState:
    def __init__(self, ticker, S, series, sigma, r, q=0.0, T=None):
        """
        A snapshot of the market for a single underlying asset.

        Parameters:
        ticker (string): stock symbol
        S (float): spot price
        sigma (float): volatility
        r (float): risk free rate
        q (float): dividend yield, (default value is 0.0)
        """
        self.ticker = ticker
        self.S = S
        self.series = series
        self.sigma = sigma
        self.r = r
        self.q = q
        self.T = T
    
    def __repr__(self):
        return f"<MarketState ticker:'{self.ticker}', S_T:{self.S:.2f}, Vol:{self.sigma:.2}, r:{self.r:.2}>"

    def apply_shock(self, delta_S_T=0.0, delta_sigma=0.0):
        """
        Returns a new MarketState with adjusted values.

        Parameters:
        delta_S_T (float): signed percentage change in spot price
        delta_sigma (float): signed percentage change in volatility

        Returns:
        MarketState: updated MarketState
        """
        return MarketState(
            ticker=self.ticker,
            S=self.S * (1 + delta_S_T),
            sigma=self.sigma + delta_sigma,
            r=self.r,
            q=self.q)
