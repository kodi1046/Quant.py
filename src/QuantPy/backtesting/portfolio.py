from __future__ import annotations

from ..instruments.option import Option, EuropeanOption, CALL, PUT
from ..instruments.option import Option
from ..instruments.equity import Equity

class Portfolio:
    """
    The portfolio class.

    Attributes
    ----------
    initial_cash: int
        The amount of cash you start with.
    cash: float
        The amount of cash you currently have.
    positions: List(Positions)
        All the active positions of the portfolio.
    history: List(Dict)
        Holds snapshots, containing information about your portfolio at a given time.
    """
    def __init__(self, initial_cash: int):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = []
        self.history = []
    
    """
    Adds a given position to the positions array.

    Parameters
    ----------
    position: Positions
        The position to append.
    """
    def add_position(self, position: Position):
        self.positions.append(position)

    """
    Removes a position from the positions array, 
    if the positions array contains it.

    Parameters
    ----------
    position: Position
        The position to remove.
    """
    def remove_position(self, position: Position):
        if position in self.positions:
            self.positions.remove(position)

    """
    Gets the total market value of the portfolio at a given market state.

    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the total market value.
    engine: Engine
        The engine(s) to use to calculate the value of an asset.

    Returns
    -------
    float
        The total market value of the portfolio at the given market state.
    """
    def mark_to_market(self, market_state: MarketState, engine: Engine):
        total_mv = 0.0
        for pos in self.positions:
            total_mv += pos.get_market_value(market_state, engine)
        return total_mv

    """
    Gets the total delta of the portfolio at a given market state.

    Parameters
    ----------
    market_state: MarketState
        The market state at which to get the total delta.
    engine: Engine
        The engine(s) to use to calculate the total delta.

    Returns
    -------
    float
        The total delta of the portfolio at the given market state.
    """
    def get_delta(self, market_state: MarketState, engine: Engine):
        total_delta = 0.0
        for pos in self.positions: # FIXME: all the positions do not use the same engine.
            total_delta += pos.get_total_delta(market_state, engine)
        return total_delta
     
    """
    Gets the total equity of the portfolio at a given market state.

    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the total equity.
    engine: Engine
        The engine to use to calculate the value of the assets.
    """
    def get_total_equity(self, market_state: MarketState, engine: Engine):
        return self.cash + self.mark_to_market(market_state, engine) # FIXME: same engine problem

    """
    Cleans up expired assets. 

    If you for example have options in your portfolio and their expiration time has passed, 
    they are no longer needed, and can be removed.

    Parameters
    ----------
    market_state: MarketState
        The market state at which to clean up, (usually this will be the current state).
    date: datetime
        the (current) date.
    """
    def cleanup_expired(self, market_state, date):
        active_positions = []
        for pos in self.positions:
            if isinstance(pos.instrument, Option):
                if pos.instrument.expiry is not None and date >= pos.instrument.expiry:
                    payoff_value = pos.instrument.payoff(market_state) * pos.quantity
                    self.cash += payoff_value
                else:
                    active_positions.append(pos)
            else:
                active_positions.append(pos)
            
        self.positions = active_positions

    """
    Records a snapshot of the market at a given state, 
    collecting metadata that can be used for analysis or visualization.

    Parameters
    ----------
    date: date
        The time at which to record the snapshot 
        (usually taken to be the current time).
    market_state: MarketState
        The market state at which to record the snapshot.
        Note that there is an implicit relation 
        between this market state and the date.
    engine: Engine
        The engine to use to calculate the price of the assets.
    
    Returns
    -------
    Dict
        A dictionary containing: 
            'date': date,
            'equity': equity,
            'cash': cash,
            'pnl_pct': (equity - initial cash) - 1,
            'delta': delta
    """
    def record_snapshot(
            self, 
            date: datetime, 
            market_state: MarketState, 
            engine: Engine):
        equity = self.get_total_equity(market_state, engine)
        delta = self.get_delta(market_state, engine) # FIXME: engine problem again.
        snapshot = {
            'date': date,
            'equity': equity,
            'cash': self.cash,
            'pnl_pct': (equity / self.initial_cash) - 1,
            'delta': delta
        }
        self.history.append(snapshot)

class Position:
    """
    The position class.

    Attributes
    ----------
    instrument: Instrument
        The instrument of the position.
    quantity: int
        The quantity to buy.
    entry_price: Float
        The entry price of the asset.
    """
    def __init__(
            self, 
            instrument: Instrument, 
            quantity: int, 
            entry_price: float):
        self.instrument = instrument
        self.quantity = quantity
        self.entry_price = entry_price
        # FIXME: Add engine here so you can use it to calculate price, delta etc.
    
    """
    Gets the price of the instrument at a given market state.

    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the price.
    engine: Engine
        The engine to use to calculate the price.

    Returns
    -------
    float
        The price of the asset at the market state.
    """
    def get_unit_price(self, market_state: MarketState, engine: Engine):
        return self.instrument.price(market_state)
    
    """
    Gets the market value of the position at a given market state.

    The market value is calculated as:
        S * quantity

    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the market value.
    engine: Engine
        The engine to use to calculate the market value.
    
    Returns
    -------
    float
        The market value of the position at the market state.
    """
    def get_market_value(self, market_state: MarketState, engine: Engine):
        return self.get_unit_price(market_state, engine) * self.quantity

    """
    Gets the unrealized pnl of the position at a given market state.

    The unrealized pnl is calculated as:
        (S - entry price) * quantity
    
    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the unrealized pnl.
    engine: Engine
        The engine to use to calculate the price of the asset.

    Returns
    -------
    float
        The unrealized pnl of the position at the market state.
    """
    def get_unrealized_pnl(self, market_state: MarketState, engine: Engine):
        return (self.get_unit_price(market_state, engine) - self.entry_price) * self.quantity

    """
    Gets the total delta of the position.

    The total delta is calculates as:
        delta * quantity
    
    Parameters
    ----------
    market_state: MarketState
        The market state at which to calculate the total delta.
    engine: Engine
        The engine to use to calculate the delta of the asset.
    
    Returns
    -------
    float
        The total delta of the position at the market state.
    """ 
    def get_total_delta(self, market_state, engine):
        unit_delta = self.instrument.delta(market_state)
        return unit_delta * self.quantity

    

