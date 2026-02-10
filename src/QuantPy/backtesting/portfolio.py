from ..instruments.option import Option, EuropeanOption, CALL, PUT

class Portfolio:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = []
        self.history = []
    
    def add_position(self, position):
        self.positions.append(position)

    def remove_position(self, position):
        self.positions.pop(position)

    def mark_to_market(self, market_state, engine):
        total_mv = 0
        for pos in self.positions:
            total_mv += pos.get_market_value(market_state, engine)
        return total_mv

    def get_greeks(self, market_state, engine):
        total_greeks = []
        for pos in self.positions:
            greeks = pos.get_greeks(market_state, engine)
            total_greeks.append(greeks)
        return total_greeks
    
    def get_total_market_value(self, market_state, engine):
        return sum(pos.get_market_value(market_state, engine) for pos in self.positions)

    def get_total_equity(self, market_state, engine):
        return self.cash + self.get_total_market_value(market_state, engine)

    def cleanup_expired(self, market_state):
        active_positions = []
        for pos in self.positions:
            if isinstance(pos.instrument, Option) and market_state.T <= 0:
                payoff_value = pos.instrument.payoff(market_state.S)
                self.cash += payoff_value * pos.quantity
            else:
                active_positions.append(pos)
            
        self.positions = active_positions

    def record_snapshot(self, date, market_state, engine):
        equity = self.get_total_equity(market_state, engine)
        greeks = self.get_greeks(market_state, engine)
        snapshot = {
            'date': date,
            'equity': equity,
            'cash': self.cash,
            'pnl_pct': (equity / self.initial_cash) - 1,
            **greeks
        }
        self.history.append(snapshot)

class Position:
    def __init__(self, instrument, quantity, entry_price):
        self.instrument = instrument
        self.quantity = quantity
        self.entry_price = entry_price
    
    def __get_unit_price(self, market_state, engine):
        return engine.calculate_price(self.instrument, market_state)
    
    def get_market_value(self, market_state, engine):
        return __get_unit_price(market_state, engine) * self.quantity

    def get_unrealized_pnl(self, market_state, engine):
        return (__get_unit_price(market_state, engine) - self.entry_price) * self.quantity

    def get_total_greeks(self, market_state, engine):
        unit_greeks = engine.calculate_greeks(market_state, engine)
        return {k: v * self.quantity for k, v in unit_greeks.items()}

