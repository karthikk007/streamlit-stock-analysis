from stock_handler.stock_ticker_data import StockTickerData

import datetime

class StockData():
    def __init__(self, ticker: StockTickerData, key, start: datetime.date, end: datetime.date):
        self.ticker: StockTickerData = ticker
        self.key = key
        self.start = start
        self.end = end
        self.data = None