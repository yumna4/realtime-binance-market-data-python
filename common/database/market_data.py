from sqlalchemy import Column, String, DateTime, Float

from common.database.base import base


class MarketData(base):
    __tablename__ = 'market_data'
    __table_args__ = {'extend_existing': True}
    timestamp = Column(DateTime,  primary_key=True)
    symbol = Column(String, primary_key=True)
    price = Column(Float)

    def __init__(self, timestamp=None, symbol=None, price=None):
        self.timestamp = timestamp
        self.symbol = symbol
        self.price = price



