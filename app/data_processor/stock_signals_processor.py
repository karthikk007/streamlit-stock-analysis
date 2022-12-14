import json
from services.cache_handler.ticker_data_handler import TickerDataHandler
from interactor.stock_interactor import get_ticker_list_for_category
from data_processor.stock_data_processor import StockDataProcessor
from data_models.ticker_data_model import TickerDataModel
from services.cache_handler.stock_tracker_handler import StockTrackingHandler
from data_models.stock_data_view_model import StockDataViewModel


import datetime, threading
from dateutil.relativedelta import relativedelta
from threading import current_thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from random import randint
from time import sleep


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

    def prefetch_records(self, category):
        text = category.split('-')

        number = int(text[1])

        ncat = None
        ncat1 = None
        pcat = None
        pcat1 = None

        if number == 0:
            n = number + 1
            n1 = n + 1

            ncat = text[0] + '-0' + str(n)
            ncat1 = text[0] + '-0' + str(n1)

        elif number == 30:
            p = number - 1
            p1 = p - 1

            pcat = text[0] + '-' + str(p)
            pcat1 = text[0] + '-' + str(p1)

        else:
            n = number + 1
            n1 = n + 1
            p = number - 1
            p1 = p - 1

            if len(str(n)) == 1:
                ncat = text[0] + '-0' + str(n)
            else:
                ncat = text[0] + '-' + str(n)

            if len(str(p)) == 1:
                pcat = text[0] + '-0' + str(p)
            else:
                pcat = text[0] + '-' + str(p)

            if p1 >= 0:
                if len(str(p1)) == 1:
                    pcat1 = text[0] + '-0' + str(p1)
                else:
                    pcat1 = text[0] + '-' + str(p1)

            if n1 <= 30:
                if len(str(n1)) == 1:
                    ncat1 = text[0] + '-0' + str(n1)
                else:
                    ncat1 = text[0] + '-' + str(n1)                    

        print('ncat = ', ncat)
        print('pcat = ', pcat)
        print('ncat1 = ', ncat1)
        print('pcat1 = ', pcat1)

        print('\n\n\n----------------------------- starting next_cat_prefetcher thread')
        next_cat_prefetcher = threading.Thread(target=self.process_records_background, args=(ncat,))
        next_cat_prefetcher.name = 'next_cat_prefetcher'

        print('\n\n\n----------------------------- starting prev_cat_prefetcher thread')
        prev_cat_prefetcher = threading.Thread(target=self.process_records_background, args=(pcat,))
        prev_cat_prefetcher.name = 'prev_cat_prefetcher'

        print('\n\n\n----------------------------- starting next_cat_prefetcher1 thread')
        next_cat_prefetcher1 = threading.Thread(target=self.process_records_background, args=(ncat1,))
        next_cat_prefetcher1.name = 'next_cat_prefetcher1'

        print('\n\n\n----------------------------- starting prev_cat_prefetcher1 thread')
        prev_cat_prefetcher1 = threading.Thread(target=self.process_records_background, args=(pcat1,))
        prev_cat_prefetcher1.name = 'prev_cat_prefetcher1'


        next_cat_prefetcher.start()
        prev_cat_prefetcher.start()
        next_cat_prefetcher1.start()
        prev_cat_prefetcher1.start()

        next_cat_prefetcher.join()
        prev_cat_prefetcher.join()
        next_cat_prefetcher1.join()
        prev_cat_prefetcher1.join()


    def process_records_background(self, category):

        if category is None:
            return

        print('\n\n')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('process_records_background for cat = ', category)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        stock_list = get_ticker_list_for_category(category)

        for i in range(1):
            with ThreadPoolExecutor(20) as executor:
                executor.map(self.populate_stock_signal, stock_list)

        print('\n\n')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ end cat = ', category)
        print('\n\n')

    def process_records(self, category):

        stock_list = get_ticker_list_for_category(category)

        # print(json.dumps(stock_list, indent=4)) 
        all_stock_list = stock_list
        skipped_list = []
        fetch_list = []


        for item in stock_list:
            ticker = item['Ticker']

            stock_signal = self.populate_stock_signal(item, download_only=False)

            if stock_signal is None:
                skipped_list.append(ticker)
                continue

            fetch_list.append(ticker)
            self.data[ticker] = stock_signal

        print('\n\n\n----------------------------- starting prefetch_records thread')
        prefetch_records = threading.Thread(target=self.prefetch_records, args=(category,))
        prefetch_records.name = 'prefetch_records'
        prefetch_records.start()

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

    def populate_stock_signal(self, item, download_only = True):

        ticker = self.tickerHandler.get_ticker_model(item['Ticker'])
        
        if not ticker:
            return None

        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=1)

        stock_data = StockDataViewModel(ticker=ticker, key="1 Year", start=start_date, end=end_date)

        stock_processor = StockDataProcessor(stock_data)
        
        try:
            print('{:30} - loading data for \t ticker = {:20} category = {:20}'.format(current_thread().name, ticker.symbol, item['CATEGORY']))
            data = stock_processor.load_data()
        except Exception as e:
            print(e)
            return None

        if len(data) < 40:
            print('\n{:30} - {} has {} only entries... Skipping....................................\n'.format(current_thread().name, ticker.symbol, len(data)))
            return None

        if not download_only:
            stock_processor.add_indicators()

        stock_signal = StockSignalsData(stock_processor.stock_data, item)

        return stock_signal


def get_track_list():
    tracker = StockTrackingHandler.instance()
    track_list = tracker.track_list()

    return track_list



    

    


