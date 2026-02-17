from ..instruments.option import Option, EuropeanOption, CALL, PUT
from ..instruments.option import Option
from ..instruments.equity import Equity

class Portfolio:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = []
        self.history = []
    
    def add_position(self, position):
        self.positions.append(position)

    def remove_position(self, position):
        if position in self.positions:
            self.positions.remove(position)

    def mark_to_market(self, market_state, engine):
        total_mv = 0
        for pos in self.positions:
            total_mv += pos.get_market_value(market_state, engine)
        return total_mv

    
    def get_delta(self, market_state, engine):
        total_delta = 0.0
        for pos in self.positions:
            total_delta += pos.get_total_delta(market_state, engine)
        return total_delta
    
    def get_total_market_value(self, market_state, engine):
        return sum(pos.get_market_value(market_state, engine) for pos in self.positions)

    def get_total_equity(self, market_state, engine):
        return self.cash + self.get_total_market_value(market_state, engine)

    def cleanup_expired(self, market_state, date):
        active_positions = []
        for pos in self.positions:
            if isinstance(pos.instrument, Option):
                if pos.instrument.expiry is not None and date >= pos.instrument.expiry:
                    payoff_value = pos.instrument.payoff(market_state.S) * pos.quantity
                    self.cash += payoff_value
                else:
                    active_positions.append(pos)
            else:
                active_positions.append(pos)
            
        self.positions = active_positions

    def record_snapshot(self, date, market_state, engine):
        equity = self.get_total_equity(market_state, engine)
        delta = self.get_delta(market_state, engine)
        snapshot = {
            'date': date,
            'equity': equity,
            'cash': self.cash,
            'pnl_pct': (equity / self.initial_cash) - 1,
            'delta': delta
        }
        self.history.append(snapshot)

class Position:
    def __init__(self, instrument, quantity, entry_price):
        self.instrument = instrument
        self.quantity = quantity
        self.entry_price = entry_price
    
    def get_unit_price(self, market_state, engine):
        return self.instrument.price(market_state)
    
    def get_market_value(self, market_state, engine):
        return self.get_unit_price(market_state, engine) * self.quantity

    def get_unrealized_pnl(self, market_state, engine):
        return (self.get_unit_price(market_state, engine) - self.entry_price) * self.quantity
    
    def get_total_delta(self, market_state, engine):
        unit_delta = self.instrument.delta(market_state)
        return unit_delta * self.quantity

    

