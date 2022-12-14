import os
import datetime
from data_models.stock_data_cache_model import StockDataCacheModel

from creation_pattern.singletion import SingletonDoubleChecked
from services.cache.stock_data_cache import StockDataCache

from threading import Lock, current_thread

import datetime
import yfinance as yf

class StockDataHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = StockDataCache()
        self.lock = Lock()

    def fetch_from_cache(self, symbol, key):

        with self.lock:

            # self.lock.acquire()
            frame = self.data_cache.cache.get(symbol)
            # self.lock.release()

            if frame is None:
                print('{:30} - cache miss for {}'.format(current_thread().name, symbol))
                return None

            value = frame.get(key)
            cache_data = None

            if value is not None:
                cache_data = StockDataCacheModel.from_json(value)

            if cache_data is None or not os.path.exists(cache_data.path):
                # print('[-------------------- StockDataCache fetch_from_cache ---- cache miss ---- ', symbol)
                return None
            else:
                # print('[-------------------- StockDataCache fetch_from_cache ++++ cache hit ++++ ', symbol)
                # self.lock.acquire()
                data = self.data_cache.get_data(cache_data.path)
                # self.lock.release()
                return data


    def update_cache(self, symbol, key, data, start: datetime, end: datetime):
        self.lock.acquire()
        self.data_cache.update_cache(symbol, key, data, start, end)
        self.lock.release()


class YFDownloader(SingletonDoubleChecked):
        def __init__(self) -> None:
            super().__init__()
            self.lock = Lock()

        def download(self, symbol, start, end):
            data = None
        
            with self.lock:
                try:
                    data = yf.download(
                            symbol, 
                            start, 
                            end + datetime.timedelta(days=1),
                            timeout=3.0
                        )

                    assert len(data) > 0
                except (AssertionError, Exception) as e:
                    print('got exception: ', e)
                    raise AssertionError("Cannot fetch data, check spelling or time window - ", symbol, start, end)

            return data