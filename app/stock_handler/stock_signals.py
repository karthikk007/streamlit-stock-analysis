
from stock_handler.stock import StockData, StockTickerData
from config.config import StockTracker
from stock_handler.stock import Stock

import datetime
from dateutil.relativedelta import relativedelta


class StockSignalsData():
    def __init__(self, stock: Stock) -> None:
        self.stock = stock


class StockSignals(object):
    buy_signals = {}
    sell_signals = {}
    data = {}

    def __init__(self) -> None:
        pass

    def process_records(self):        
    
        for key, value in get_track_list().items():

            stock_signal = self.populate_stock_signal(key, value)
            self.data[key] = stock_signal

        self.process_signals()

    def process_signals(self):
        for key, value in self.data.items():
            if self.is_buy_signal(value):
                self.buy_signals[key] = value
            
            if self.is_sell_signal(value):
                self.sell_signals[key] = value


    def is_buy_signal(self, data: StockSignalsData):
        is_buy_signal = False

        df = data.stock.stock_data.data
        df_lookup = df.iloc[-5:]

        for x in df_lookup["buy_signal"]:
            if x:
                is_buy_signal = True
                break
        
        return is_buy_signal

    def is_sell_signal(self, data: StockSignalsData):
        is_sell_signal = False

        df = data.stock.stock_data.data
        df_lookup = df.iloc[-5:]

        for i in df_lookup["sell_signal"]:
            if i:
                is_sell_signal = True
                break
        
        return is_sell_signal

    def populate_stock_signal(self, key, value):

        ticker = StockTickerData(key, value)
        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=1)
        stock_data = StockData(ticker=ticker, key="1 Year", start=start_date, end=end_date)

        stock = Stock(stock_data=stock_data)
        
        stock.load_data()
        stock.add_indicators()

        stock_signal = StockSignalsData(stock)

        return stock_signal


def get_track_list():
    tracker = StockTracker()
    track_list = tracker.track_list

    return track_list

    

    


