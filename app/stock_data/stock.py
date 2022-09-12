import datetime
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from graph_utils import plot_stock, cufflinks_plot_stock 
from data_source.data_fetcher import StockDataFetcher

data_fetcher = StockDataFetcher()

class Stock():
    """
    This class enables data loading, plotting and statistical analysis of a given stock,
     upon initialization load a sample of data to check if stock exists. 
        
    """

    def __init__(self, symbol, start: datetime.date, end: datetime.date):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    # @st.cache(show_spinner=True) #Using st.cache allows st to load the data once and cache it. 
    def load_data(self, start: datetime.date = None, end: datetime.date = None, inplace=True):   
        data = data_fetcher.load_data(self.symbol, start, end, inplace) if start is not None else data_fetcher.load_data(self.symbol, self.start, self.end, inplace)

        data = data.dropna()

        if inplace:
            self.data = data
            self.start = start if start is not None else self.start
            self.end = end if end is not None else self.end

        return data


    def add_macd(self):
        # https://www.alpharithms.com/calculate-macd-python-272222/
        # Calculate MACD values using the pandas_ta library
        
        self.data.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
        

    def add_rsi(self):
        length = 8
        self.data.ta.rsi(close='close', length=length, append=True, signal_indicators=True, xa=60, xb=40, drift=3)

    
    def add_sma_volume(self):
        # Add indicators, using data from before
        self.data.ta.sma(close='volume', length=50, append=True)
    
    def add_stochastic(self):
        # Add some indicators
        self.data.ta.stoch(high='high', low='low', k=14, d=3, append=True)

    def plot_raw_data(self):
        fig = go.Figure()

        self.add_macd()
        self.add_rsi()
        self.add_sma_volume()
        self.add_stochastic()

        # View result
        pd.set_option("display.max_columns", None)  # show all columns

        # Force lowercase (optional)
        self.data.columns = [x.lower() for x in self.data.columns]

        return plot_stock.plot_macd(fig, self.data, 8)

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
        i = self.start
        j = self.end
        # s = self.data.query("date==@i")['close'].values[0]
        # e = self.data.query("date==@j")['close'].values[0]
        e = self.data.tail(1)['close'].values[0]
        s = self.data.head(1)['close'].values[0]


        difference = round(e - s, 2)
        change = round(difference / (s + epsilon) * 100, 2)
        e = round(e, 2)
        cols = st.columns(2)
        (color, marker) = ("green", "+") if difference >= 0 else ("red", "")

        cols[0].markdown(
            f"""<p style="font-size: 90%;margin-left:5px">{self.symbol}: {e}</p>""",
            unsafe_allow_html=True)
        
        cols[1].markdown(
            f"""<p style="color:{color};font-size:90%;margin-right:5px">{marker}{difference} &emsp; {marker}{change}% </p>""",
            unsafe_allow_html=True) 