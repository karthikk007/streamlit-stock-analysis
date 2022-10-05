from data_handler.data_fetcher import DataFetcher

from nsetools import Nse
from cache_handler.ticker_data_cache import TickerDataCache

class TickerDataFetcher(DataFetcher):
    
    def __init__(self):
        super().__init__()
        self.nse = Nse()
        self.data_cache = TickerDataCache()
        self.all_stock_codes = {}

    def load_ticker_list(self):

        data = None
        cache_data = self.data_cache.cache

        if cache_data is not None and len(cache_data) > 0:
             data = cache_data
        else:
            data = self.nse.get_stock_codes()

            try:
                assert len(data) > 0
            except AssertionError:
                print("Cannot fetch data, check spelling or time window")
            
            self.data_cache.update_cache(data)

        self.all_stock_codes = data
