import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from ...data.loader import DataFetcher
from ...data.processor import MarketProcessor
from ...data.state import MarketState
from ...backtesting.backtest import Backtest
from ...backtesting.strategy import DeltaHedgeStrategy
from ...instruments.option import EuropeanOption, CALL

def main(instrument, engine):
    """
    Delta hedging backtest, hedging AAPL stock, using a european call option, which uses black scholes for pricing
    """
    TICKER       = "AAPL"
    START_DATE   = datetime(2025, 1, 1)
    END_DATE     = datetime(2026, 2, 1)
    INITIAL_CASH = 10000

    OPTION_K       = instrument.K
    OPTION_T_years = instrument.T
    OPTION_TYPE    = instrument.option_type
    OPTION_QTY     = 10
    EXPIRY_DATE  = START_DATE + timedelta(days=int(OPTION_T_years * 365.25))

    DELTA_THRESHOLD = 5.0

    close_series = DataFetcher.get_historical_data(
        ticker=TICKER,
        start_date=START_DATE,
        end_date=END_DATE
    )

    processor = MarketProcessor(close_series)

    realized_vol = processor.get_realized_volatility()
    print(f"realized volatility: {realized_vol:.4f}")

    r = DataFetcher.get_risk_free_rate()
    print(f"risk-free rate: {r:.4f}")

    price_series = close_series.to_dict()

    option = EuropeanOption(
        K = OPTION_K,
        T = OPTION_T_years,
        option_type = OPTION_TYPE,
        expiry=EXPIRY_DATE
    )
    option.set_engine(engine)

    strategy = DeltaHedgeStrategy(
        instrument=option,
        quantity=OPTION_QTY,
        engine=engine,
        params={'threshold': DELTA_THRESHOLD}
    )

    bt = Backtest(
        ticker=TICKER,
        price_series=price_series,
        r=r,
        sigma=realized_vol
    )

    print("starting backtest...")
    bt.run(strategy=strategy, engine=engine)
    print("backtest complete.")

    history = bt.portfolio.history

    if not history:
        print("no snapshots recorded")
    else:
        df = pd.DataFrame(history).set_index('date')

        fig, axes = plt.subplots(3, 1, figsize=(13, 19), sharex=True, gridspec_kw={'height_ratios': [4, 2.5, 1.5]})

        # equity & cash
        ax1 = axes[0]
        ax1.plot(df.index, df['equity'], label='Portfolio Equity', color='#1f77b4', lw=1.6)
        ax1.plot(df.index, df['cash'], label='Cash', color='#2ca02c', alpha=0.7, lw=1.1)
        ax1.set_title(f'Delta-Hedged {OPTION_QTY} {TICKER} {OPTION_TYPE} K={OPTION_K} – Real Data')
        ax1.set_ylabel('Value ($)')
        ax1.legend()
        ax1.grid(alpha=0.3)

        # underlying price
        ax2 = axes[1]
        underlying_prices = [
            price_series[TICKER].get(date, np.nan) 
            for date in df.index
        ]
        ax2.plot(df.index, underlying_prices, color='#ff7f0e', label='Underlying Close')
        ax2.set_ylabel('Price ($)')
        ax2.legend()
        ax2.grid(alpha=0.3)

        # net delta
        ax3 = axes[2]
        ax3.plot(df.index, df.get('delta', pd.Series(0, index=df.index)),
                color='#9467bd', label='Net Portfolio Delta')
        ax3.axhline(0, color='gray', ls='--', alpha=0.6)
        ax3.set_ylabel('Delta')
        ax3.set_xlabel('Date')
        ax3.legend()
        ax3.grid(alpha=0.3)

        plt.tight_layout()
        plt.show()

        # quick stats
        final_equity = df['equity'].iloc[-1]
        pnl_pct = (final_equity / INITIAL_CASH - 1) * 100
        print(f"Final equity: ${final_equity:,.2f}  →  PnL: {pnl_pct:+.2f}%")



if __name__ == '__main__':
    instrument1 = EuropeanOption(240, 0.5, CALL)
    engine1 = instrument1.BlackScholes()
    # main(instrument1, engine1)

    instrument2 = instrument1
    engine2 = instrument1.MonteCarlo(num_simulations=10000)
    main(instrument2, engine2)