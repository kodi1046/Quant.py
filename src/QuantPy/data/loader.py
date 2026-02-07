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

