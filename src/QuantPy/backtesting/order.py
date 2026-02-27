from enum import Enum
from ..instruments.base import Instrument

class OrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class Order:
    def __init__(self, side, instrument, quantity):
        self.side = side
        self.instrument = instrument
        self.quantity = quantity

