import json
from services.cache_handler.ticker_data_handler import TickerDataHandler
from interactor.stock_interactor import get_ticker_list_for_category
from data_processor.stock_data_processor import StockDataProcessor
from data_models.ticker_data_model import TickerDataModel
from services.cache_handler.stock_tracker_handler import StockTrackingHandler
from data_models.stock_data_view_model import StockDataViewModel


import datetime
from dateutil.relativedelta import relativedelta


class StockSignalsData():
    def __init__(self, stock: StockDataViewModel, screening_data = None) -> None:
        self.stock = stock
        self.screening_data = screening_data

    def get_ticker(self):
        return self.stock.ticker


class StockSignalProcessor(object):
    signal_delta = 10
    signal_treshold = 0.5

    def __init__(self) -> None:
        self.buy_signals = {}
        self.sell_signals = {}
        self.data = {}

        self.tickerHandler = TickerDataHandler()

    def get_stock_list(self, category):
        stock_list = get_ticker_list_for_category(category)

        return stock_list

    def process_records(self, category):
        stock_list = get_ticker_list_for_category(category)

        # print(json.dumps(stock_list, indent=4)) 
        all_stock_list = stock_list
        skipped_list = []
        fetch_list = []


        for item in stock_list:
            ticker = item['Ticker']

            stock_signal = self.populate_stock_signal(item)

            if stock_signal is None:
                skipped_list.append(ticker)
                continue

            fetch_list.append(ticker)
            self.data[ticker] = stock_signal

        self.process_signals()

        return (all_stock_list, skipped_list, fetch_list)

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

        sell_lookup = df.iloc[-5:]
        for x in sell_lookup["sell_signal"]:
            if x:
                return is_buy_signal

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

        buy_lookup = df.iloc[-5:]
        for x in buy_lookup["buy_signal"]:
            if x:
                return is_sell_signal

        sell_count = 0
        for x in df_lookup["sell_signal"]:
            if x:
                sell_count += 1
            
            if sell_count >= self.signal_delta * self.signal_treshold:
                is_sell_signal = True
                break
        
        return is_sell_signal

    def populate_stock_signal(self, item):

        ticker = self.tickerHandler.get_ticker_model(item['Ticker'])
        
        if not ticker:
            return None

        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=1)
        stock_data = StockDataViewModel(ticker=ticker, key="1 Year", start=start_date, end=end_date)

        stock_processor = StockDataProcessor(stock_data)
        
        data = stock_processor.load_data()

        if len(data) < 40:
            print('\n{} has {} only entries... Skipping....................................\n'.format(ticker.symbol, len(data)))
            return None


        stock_processor.add_indicators()

        stock_signal = StockSignalsData(stock_processor.stock_data, item)

        return stock_signal


def get_track_list():
    tracker = StockTrackingHandler.instance()
    track_list = tracker.track_list()

    return track_list



    

    


