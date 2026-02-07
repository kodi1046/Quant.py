
class MarketState:
    def __init__(S_T, sigma, r, q=0.0):
        """
        A snapshot of the market for a single underlying asset.

        Parameters:
        S_T (float): spot price
        sigma (float): volatility
        r (float): risk free rate
        q (float): dividend yield, (default value is 0.0)
        """
        self.S_T = S_T
        self.sigma = sigma
        self.r = r
        self.q = q
    
    def __repr__(self):
        return f"<MarketState S_T:{self.S_T:.2f}, Vol:{self.sigma:.2%}, r:{self.r:.2%}>"

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
            S_T=self.S_T * (1 + delta_S_T),
            sigma=self.sigma + delta_sigma,
            r=self.r,
            q=self.q)
