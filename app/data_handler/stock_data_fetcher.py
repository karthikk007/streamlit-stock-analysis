from cache_handler.stock_data_cache import StockDataCache
from data_handler.data_fetcher import DataFetcher
import datetime
import yfinance as yf

class StockDataFetcher(DataFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.data_cache = StockDataCache()

    # @st.cache(show_spinner=True) #Using st.cache allows st to load the data once and cache it. 
    def load_data(self, symbol, key, start: datetime.date, end: datetime.date, inplace=False):
        """
        takes a start and end dates, download data do some processing and returns dataframe
        """

        data = None
        cache_data = self.data_cache.fetch_from_cache(symbol, key)

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

            data = yf.download(symbol, start, end + datetime.timedelta(days=1))

            #Check if there is data
            try:
                assert len(data) > 0
                self.data_cache.update_cache(symbol, key, data, start, end)
            except AssertionError:
                print("Cannot fetch data, check spelling or time window")


        data.reset_index(inplace=True)

        data.rename(columns={"Date": "datetime"}, inplace=True)

        data["date"] = data.apply(lambda raw: raw["datetime"], axis=1)

        return data
            