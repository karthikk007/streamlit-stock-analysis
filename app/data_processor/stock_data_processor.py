import datetime
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from services.data_fetcher.stock_data_fetcher import StockDataFetcher

from graph_utils.plot_stock import plot_macd
from graph_utils.plot_stock import UP_COLOR, DOWN_COLOR

from data_models.stock_data_view_model import StockDataViewModel


class StockDataProcessor():
    """
    This class enables data loading, plotting and statistical analysis of a given stock,
     upon initialization load a sample of data to check if stock exists. 
        
    """

    def __init__(self, stock_data: StockDataViewModel):
        self.data_fetcher = StockDataFetcher()
        self.stock_data = stock_data

    # @st.cache(show_spinner=True) #Using st.cache allows st to load the data once and cache it. 
    def load_data(self, start: datetime.date = None, end: datetime.date = None, inplace=True):
        ticker = self.stock_data.ticker
        symbol = ticker.symbol + '.NS'
        key = self.stock_data.key

        try:
            data = self.data_fetcher.load_data(self.stock_data, inplace) 
        except Exception as e:
            raise e

        data = data.dropna()

        if inplace:
            self.stock_data.data = data
            self.stock_data.start = start if start is not None else self.stock_data.start
            self.stock_data.end = end if end is not None else self.stock_data.end

        return data


    def add_macd(self):
        # https://www.alpharithms.com/calculate-macd-python-272222/
        # Calculate MACD values using the pandas_ta library
        
        self.stock_data.data.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
        

    def add_rsi(self):
        length = 8
        self.stock_data.data.ta.rsi(close='close', length=length, append=True, signal_indicators=True, xa=60, xb=40, drift=3)

    
    def add_sma_volume(self):
        # Add indicators, using data from before
        self.stock_data.data.ta.sma(close='volume', length=50, append=True)
    
    def add_stochastic(self):
        # Add some indicators
        self.stock_data.data.ta.stoch(high='high', low='low', k=14, d=3, append=True)

    def add_indicators(self):
        print('adding indicators to ', self.stock_data.ticker.symbol)

        self.add_macd()
        self.add_rsi()
        self.add_sma_volume()
        self.add_stochastic()

        # View result
        pd.set_option("display.max_columns", None)  # show all columns

        # Force lowercase (optional)
        self.stock_data.data.columns = [x.lower() for x in self.stock_data.data.columns]

        self.color_volume()
        self.add_buy_signal()
        self.add_sell_signal()


    def plot_raw_data(self):
        fig = go.Figure()

        self.add_indicators()

        return plot_macd(fig, self.stock_data.data, 8)

        # return plot_stock.plot_stock_close(fig, self.data, self.symbol)

        # cufflinks_plot_stock.cf_plot_candlestick(
        #     self.data,
        #     self.symbol
        # )
        # return cufflinks_plot_stock.cf_plot_candlestick(self.data, self.symbol)

    @staticmethod
    def nearest_business_day(DATE: datetime.date):
        """
        Takes a date and transform it to the nearest business day, 
        static because we would like to use it without a stock object.
        """

        if DATE.weekday() == 5:
            DATE = DATE - datetime.timedelta(days=1)

        if DATE.weekday() == 6:
            DATE = DATE - datetime.timedelta(days=2)
        return DATE
    
    def show_delta(self):
        """
        Visualize a summary of the stock change over the specified time period
        """

        epsilon = 1e-6
        i = self.stock_data.start
        j = self.stock_data.end
        # s = self.data.query("date==@i")['close'].values[0]
        # e = self.data.query("date==@j")['close'].values[0]
        e = self.stock_data.data.tail(1)['close'].values[0]
        s = self.stock_data.data.head(1)['close'].values[0]


        difference = round(e - s, 2)
        change = round(difference / (s + epsilon) * 100, 2)
        e = round(e, 2)
        cols = st.columns(2)
        (color, marker) = ("green", "+") if difference >= 0 else ("red", "")

        cols[0].markdown(
            f"""<p style="font-size: 90%;margin-left:5px">{self.stock_data.ticker.symbol}: {e}</p>""",
            unsafe_allow_html=True)
        
        cols[1].markdown(
            f"""<p style="color:{color};font-size:90%;margin-right:5px">{marker}{difference} &emsp; {marker}{change}% </p>""",
            unsafe_allow_html=True) 

    def color_volume(self):
        df = self.stock_data.data

        df['diff'] = df['close'] - df['open']
        df.loc[df['diff']>=0, 'color'] = UP_COLOR
        df.loc[df['diff']<0, 'color'] = DOWN_COLOR

    def add_buy_signal(self):
        buy_threshold = 20
        df = self.stock_data.data

        df.loc[
            np.logical_and(
                df['rsi_8_b_40']==1,
                df['stochk_14_3_3']<=buy_threshold,
                df['stochd_14_3_3']<=buy_threshold,
            ), 'buy_signal'] = True

        df['buy_signal'].fillna(False, inplace=True)

    def add_sell_signal(self):
        sell_threshold = 80
        df = self.stock_data.data

        df.loc[
            np.logical_and(
                df['rsi_8_a_60']==1,
                df['stochk_14_3_3']>=sell_threshold,
                df['stochd_14_3_3']>=sell_threshold,
            ), 'sell_signal'] = True

        df['sell_signal'].fillna(False, inplace=True)
