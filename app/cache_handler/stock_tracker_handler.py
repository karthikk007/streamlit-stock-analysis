
from cache.stock_tracker_cache import StockTrackerCache
from creation_pattern.singletion import SingletonDoubleChecked


class StockTrackingHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = StockTrackerCache()


    def add_stocks(self, stock_list):
        self.data_cache.update_cache(stock_list)


    def remove_stocks(self, stock_list):
        self.data_cache.remove_stocks(stock_list)


    def save(self):
        self.data_cache.save_cache()
    
    def track_list(self):
        return self.data_cache.cache
