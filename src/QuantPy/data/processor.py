import numpy as np
import pandas as pd

class MarketProcessor:
    def __init__(self, price_series: pd.DataFrame):
        self.prices = price_series
    
    def calculate_log_returns(self):
        """
       Computes the continuously compounded (log) returns of the price series.
    
        The log return is calculated as:

            ln(S_t / S_{t-1})
        
        Where S_t is the price at time t.
        
        Returns 
        -------
        pd.DataFrame
            A DataFrame of log returns with the same columns as `self.prices`.
            The first row is removed due to shifting. Any rows containing
            missing values are dropped.
        
        Notes
        -----
        - Log returns are computed column-wise.
        - Prices must be strictly positive.
        - If any column contains NaN values in a row, that entire row
          will be removed due to `.dropna()`.
        """
        return np.log(self.prices / self.prices.shift(1)).dropna()
    
    def get_realized_volatility(self, window=252): # annualized by default
        """
        Computes the annualized relized volatility from the log returns.

        Volatility is calculated as:

            annualized_vol = std(log_returns) * sqrt(window)
            
        Parameters
        ----------
        window: int, optional
            The annualized factor, typically the number of trading days in a year.
            Default is 252 (1 business year).
        
        Returns
        -------
        float
            Annualized volatility computed from the last column of the
            log returns DataFrame.
        
        Notes
        -----
        - Log returns are computes with `calculate_log_returns()`.
        - The `window` parameter scales the standard deviation to an annualized value. 

        """
        returns = self.calculate_log_returns()
        return (returns.std() * np.sqrt(window)).iloc[-1].item()

