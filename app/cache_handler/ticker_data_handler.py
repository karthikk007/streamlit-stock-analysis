from cache.ticker_data_cache import TickerDataCache
from creation_pattern.singletion import SingletonDoubleChecked


class TickerDataHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = TickerDataCache()


    def update_ticker(self, ticker_list):
        self.data_cache.update_cache(ticker_list)

    
    def get_tickers(self):
        return self.data_cache.cache