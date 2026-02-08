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
        
        data = yf.download(ticker, start=start_date, end=end_date, progress=False) # pandas DataFrame
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        return data['Close'] # subject to change

    @staticmethod
    def get_risk_free_rate(target_date=None):
        ticker = "^IRX"

        if target_date is None:
            end_date = pd.Timestamp.now()
        else:
            end_date = pd.to_datetime(target_date)
        
        start_date = end_date - pd.Timedelta(days=10)

        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                data = yf.download(ticker, period="5d", progress=False)
            
            if data.empty:
                raise ValueError("Could not retrieve risk free rate")

            latest_yield = data['Close'].dropna().iloc[-1].item()

            return latest_yield / 100
    
        except Exception as e:
            print(f"Warning: Failed to fetch RF rate ({e}). Falling back to 4.0%.")
            return 0.04
        