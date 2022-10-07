from data_processor.stock_data_processor import StockDataProcessor
from data_models.ticker_data_model import TickerDataModel
from cache_handler.stock_tracker_handler import StockTrackingHandler
from data_models.stock_data_view_model import StockDataViewModel


import datetime
from dateutil.relativedelta import relativedelta


class StockSignalsData():
    def __init__(self, stock: StockDataViewModel) -> None:
        self.stock = stock

    def get_ticker(self):
        return self.stock.ticker


class StockSignalProcessor(object):
    signal_delta = 10
    signal_treshold = 0.5

    def __init__(self) -> None:
        self.buy_signals = {}
        self.sell_signals = {}
        self.data = {}

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

        df = data.stock.data
        df_lookup = df.iloc[-self.signal_delta:]

        buy_count = 0
        for x in df_lookup["buy_signal"]:
            if x:
                buy_count += 1
            
            if buy_count >= self.signal_delta * self.signal_treshold:
                is_buy_signal = True
                break
        
        return is_buy_signal

    def is_sell_signal(self, data: StockSignalsData):
        is_sell_signal = False

        df = data.stock.data
        df_lookup = df.iloc[-self.signal_delta:]

        sell_count = 0
        for x in df_lookup["sell_signal"]:
            if x:
                sell_count += 1
            
            if sell_count >= self.signal_delta * self.signal_treshold:
                is_sell_signal = True
                break
        
        return is_sell_signal

    def populate_stock_signal(self, key, value):

        ticker = TickerDataModel(key, value)
        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=1)
        stock_data = StockDataViewModel(ticker=ticker, key="1 Year", start=start_date, end=end_date)

        stock_processor = StockDataProcessor(stock_data)
        
        stock_processor.load_data()
        stock_processor.add_indicators()

        stock_signal = StockSignalsData(stock_processor.stock_data)

        return stock_signal


def get_track_list():
    tracker = StockTrackingHandler.instance()
    track_list = tracker.track_list()

    return track_list

    

    


