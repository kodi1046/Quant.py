import yfinance as yf
import pandas as pd
import numpy as np

class DataFetcher:

    @staticmethod
    def get_historical_data(ticker, start_date, end_date):
        """
        Fetches OHLCV data from yfinance

        Parameters:
        ticker (string): the stock symbol, e.g. "AAPL", or "TSLA"
        start_time (string): the start date of the data, e.g. "2020-01-12"
        end_date (string): the end date of the data, e.g. "2024-06-01"

        Returns:
        data (pandas Series): series containing the adjusted closing prices,
                              for the given asset, for each date in the range
        """
        
        data = yf.download(ticker, start=start_date, end=end_date) # pandas DataFrame
        if date.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        return data['Adj Close'] # subject to change

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
