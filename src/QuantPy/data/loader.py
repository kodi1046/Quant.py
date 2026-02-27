import yfinance as yf
import pandas as pd
import numpy as np

from datetime import datetime

class DataFetcher:

    @staticmethod
    def get_historical_data(ticker: str, start_date: datetime, end_date: datetime):
        """
        Fetches OHLCV data from yfinance.

        Parameters
        ----------
        ticker: string 
            The stock symbol, e.g. "AAPL", or "TSLA".
        start_time: datetime 
            The start date of the data, e.g. 2020-01-12.
        end_date: datetime 
            The end date of the data, e.g. 2024-06-01.

        Returns
        -------
        pd.DataFrame 
            DataFrame containing the adjusted closing prices, 
            for the given asset, for each date in the range.
        """
        
        data = yf.download(ticker, start=start_date, end=end_date, progress=False) # pandas DataFrame
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        CLOSING_PRICES = 'Close'
        return data[CLOSING_PRICES]

    @staticmethod
    def get_risk_free_rate(target_date=None):
        """
        Retrieves the U.S. 13-week Treasury Bill yield (^IRX) from Yahoo Finance
        and returns it as a decimal risk-free rate.

        The function searches for the most recent available closing yield within
        a 10-day window ending at `target_date`. If `target_date` is None,
        the current date is used.

        Parameters
        ----------
        target_date: datetime 
            The end date for the yield lookup window. If None, uses the
            current timestamp. The function looks back 10 days from this date.

        Returns
        -------
        float 
            The latest available 13-week T-bill yield expressed as a decimal
            (e.g., 0.0525 for 5.25%). If data retrieval fails for any reason,
            the function returns a fallback value of 0.04 (4%).     
        """
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
        