import datetime
import streamlit as st
import plotly.graph_objects as go

from graph_utils import plot_stock
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

    def plot_raw_data(self):
        fig = go.Figure()
        return plot_stock.plot_stock_close(fig, self.data, self.symbol)

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
        # s = self.data.query("date==@i")['Close'].values[0]
        # e = self.data.query("date==@j")['Close'].values[0]
        e = self.data.tail(1)['Close'].values[0]
        s = self.data.head(1)['Close'].values[0]


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