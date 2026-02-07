import numpy as np

class MarketProcessor:
    def __init__(self, price_series):
        self.prices = price_series
    
    def calculate_log_returns(self):
        """
        Calculates the log returns for each entry in the series
        Formula:
            ln(price_t / price_{t-1})
        """
        return np.log(self.prices / self.prices.shift(1)).dropna()
    
    def get_realized_volatility(self, window=252): # annualized by default
        """
        Calculates (annualized) volatility 
        Formula:
            std_dev(returns) * sqrt(trading_days)
        
        Parameters:
        window (int): represents the time window, 252 by default, 
                      to represrent 1 trading year
        """
        returns = self.calculate_log_returns()
        return returns.std() * np.sqrt(window)
