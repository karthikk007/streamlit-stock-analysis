
from cache_handler.stock_tracker_cache import StockTrackerCache



class StockTracker(object):

    def __init__(self) -> None:
        self.data_cache = StockTrackerCache()
        self.track_list = self.data_cache.cache


    def save_list(self):
        self.data_cache.cache = self.track_list
        self.data_cache.save_cache()


    def add_stocks(self, stock_list):
        self.track_list.update(stock_list)


    def remove_stocks(self, stock_list):
        [self.track_list.pop(key) for key in stock_list.keys()]

