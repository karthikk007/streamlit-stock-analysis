 
from .data_fetcher import DataFetcher
from services.cache_handler.stock_data_handler import StockDataHandler, YFDownloader
from data_models.stock_data_view_model import StockDataViewModel

import datetime
import yfinance as yf

from threading import current_thread, Lock
from random import randint
from time import sleep

class StockDataFetcher(DataFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.cache_handler = StockDataHandler.instance()
        self.downloader = YFDownloader.instance()


    # @st.cache(show_spinner=True) #Using st.cache allows st to load the data once and cache it. 
    def load_data(self, stock_data_request: StockDataViewModel, inplace=False, is_fallback = False, retry_count = 0):
        """
        takes a start and end dates, download data do some processing and returns dataframe
        """

        data = None

        exchange = '.NS'

        if is_fallback:
            exchange = '.BO'

        symbol = stock_data_request.ticker.symbol + exchange
        key = stock_data_request.key
        start = stock_data_request.start
        end = stock_data_request.end

        # cache_data = self.cache_handler.fetch_from_cache(symbol, key)

        cache_data = self.data_from_cache(stock_data_request.ticker.symbol, key)

        if cache_data is not None and len(cache_data) > 0:
            data = cache_data
        else:
            # delta = end - start
            # year_old = datetime.datetime.now() - datetime.timedelta(days=365)
            # delta_date = datetime.datetime.now() - datetime.timedelta(days=delta.days)
            # if delta_date > year_old:
            #     print('under 1 year')
            #     data = yf.download(symbol, start, end + datetime.timedelta(days=1), interval='30m')
            # else:
            #     data = yf.download(symbol, start, end + datetime.timedelta(days=1))

            #Check if there is data
            try:

                print('{:30} - load data from yf \t {} - {} - {}'.format(current_thread().name, symbol, start, end))

                data = self.downloader.download(symbol, start, end)

                assert len(data) > 0
                print('{:30} - updating cache - \t {}'.format(current_thread().name, symbol))
                self.cache_handler.update_cache(symbol, key, data, start, end)
            except (AssertionError, Exception) as e:
                print(e)

                if not is_fallback and not self.is_script_runner():
                    print('{:30} - Falling back to BSE exchange - {}'.format(current_thread().name, symbol))
                    return self.load_data(stock_data_request, inplace, True, retry_count=retry_count)
                else:
                    print("{:30} - Cannot fetch data, check spelling or time window - {}".format(current_thread().name, symbol))
                    if not self.is_script_runner() and retry_count < 1:
                        self.sleep_random(2000)
                        return self.load_data(stock_data_request, inplace, is_fallback=False, retry_count=retry_count+1)
                    else:
                        raise AssertionError("Cannot fetch data, check spelling or time window")


        data.reset_index(inplace=True)

        data.rename(columns={"Date": "datetime"}, inplace=True)

        data["date"] = data.apply(lambda raw: raw["datetime"], axis=1)

        return data

    def data_from_cache(self, symbol, key, exchange='.NS'):
        sym = symbol + exchange
        cache_data = self.cache_handler.fetch_from_cache(sym, key)

        if cache_data is not None and len(cache_data) > 0:
            return cache_data
        elif exchange == '.BO':
            return None
        else:
            return self.data_from_cache(symbol, key, '.BO')


    def is_script_runner(self):
        if 'ScriptRunner' in current_thread().name:
            return True
        else:
            return False


    def sleep_random(self, max=2000):
        if not 'ScriptRunner' in current_thread().name:
            random_sleep = randint(0, max) / 1000
            print('{:30} - sleeping for {} sec'.format(current_thread().name, random_sleep))
            sleep(random_sleep)
            