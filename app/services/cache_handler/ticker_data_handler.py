from services.cache.ticker_data_cache import TickerDataCache
from creation_pattern.singletion import SingletonDoubleChecked
from data_models.ticker_data_model import TickerDataModel


class TickerDataHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = TickerDataCache()


    def update_ticker(self, ticker_list):
        self.data_cache.update_cache(ticker_list)

    
    def get_tickers(self):
        return self.data_cache.cache

    def get_ticker_model(self, ticker):
        value = self.data_cache.cache.get(ticker, None)

        if value:
            return TickerDataModel(ticker, value)
        else:
            return None
