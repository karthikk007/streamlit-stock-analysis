import os
import datetime
from data_models.stock_data_cache_model import StockDataCacheModel

from creation_pattern.singletion import SingletonDoubleChecked
from services.cache.stock_data_cache import StockDataCache


class StockDataHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = StockDataCache()


    def fetch_from_cache(self, symbol, key):

        frame = self.data_cache.cache.get(symbol)

        if frame is None:
            print('cache miss for', symbol)
            return None

        value = frame.get(key)
        cache_data = None

        if value is not None:
            cache_data = StockDataCacheModel.from_json(value)

        if cache_data is None or not os.path.exists(cache_data.path):
            print('[-------------------- StockDataCache fetch_from_cache ---- cache miss ---- ', symbol)
            return None
        else:
            print('[-------------------- StockDataCache fetch_from_cache ++++ cache hit ++++ ', symbol)
            data = self.data_cache.get_data(cache_data.path)
            return data


    def update_cache(self, symbol, key, data, start: datetime, end: datetime):
        self.data_cache.update_cache(symbol, key, data, start, end)