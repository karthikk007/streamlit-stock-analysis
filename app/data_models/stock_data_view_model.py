from data_models.ticker_data_model import TickerDataModel

import datetime

class StockDataViewModel():
    def __init__(self, ticker: TickerDataModel, key, start: datetime.date, end: datetime.date):
        self.ticker: TickerDataModel = ticker
        self.key = key
        self.start = start.date()
        self.end = end.date()
        self.data = None