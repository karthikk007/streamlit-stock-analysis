from services.data_fetcher.data_fetcher import DataFetcher
from services.cache_handler.ticker_data_handler import TickerDataHandler

from nsetools import Nse

import pandas as pd

class TickerDataFetcher(DataFetcher):
    
    def __init__(self):
        super().__init__()
        self.cache_handler = TickerDataHandler.instance()

        self.nse = Nse()
        self.all_stock_codes = {}

    def load_ticker_list(self):

        data = None
        cache_data = self.cache_handler.get_tickers()

        if cache_data is not None and len(cache_data) > 0:
             data = cache_data
        else:
            data = self.nse.get_stock_codes()

            try:
                assert len(data) > 0
            except AssertionError:
                print("Cannot fetch data, check spelling or time window")
            
            self.cache_handler.update_ticker(data)

        self.all_stock_codes = data

    def get_df_dict(self):
        df = pd.DataFrame(self.all_stock_codes.items())
        header_row = df.iloc[0]

        if header_row[0] != 'SYMBOL':
            df.loc[-1] = ['SYMBOL', 'NAME OF COMPANY']  # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index()
            header_row = df.iloc[0]
        
        df2 = pd.DataFrame(df.values[1:], columns=header_row)

        # st.table(df2)
        	
        symbol_dict = df2.set_index('SYMBOL').to_dict()['NAME OF COMPANY']

        return symbol_dict