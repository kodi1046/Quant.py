import pandas as pd
class MarketState:
    """
    A snapshot of the market for a single underlying asset.

    Attributes
    ----------
    ticker: str
        The asset symbol (e.g. 'AAPL').
    S: float
        Current spot price for the underlying asset.
    series: pd.DataFrame
        Historical price series of the underlying asset.
    sigma: float
        Volatility of the underlying asset, expressed as a decimal.
    r: float
        The risk-free rate, expressed as a decimal.
    q: float, optional
        Dividend yield, expressed as a decimal. Default is 0.0
    T: float, optional
        FIXME: should be moved to option
        Remaining time on an option (should move this to option). Default is None
    path: pd.DataFrame, optional
        A asset price path of the underlying asset. Default is None

    """
    def __init__(
            self, 
            ticker: str, 
            S: float, 
            series: pd.DataFrame, 
            sigma: float, 
            r: float, 
            q: float=0.0, 
            T: float=None, 
            path: pd.DataFrame=None):
        self.ticker = ticker
        self.S = S
        self.series = series
        self.sigma = sigma
        self.r = r
        self.q = q
        self.T = T
        self.path = path
    
    def __repr__(self):
        return f"<MarketState ticker:'{self.ticker}', S_T:{self.S:.2f}, Vol:{self.sigma:.2}, r:{self.r:.2}>"

