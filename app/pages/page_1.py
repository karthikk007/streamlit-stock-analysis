# Contents of ~/my_app/pages/page_2.py
import streamlit as st
from config.config import BuyTracker
from data_source.ticker import Ticker
import pandas as pd

def app():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

    ticker = Ticker()
    buy_tracker = BuyTracker()

    with st.spinner('loading...'):
        ticker.load_ticker_list()

        df = pd.DataFrame(ticker.all_stock_codes.items())
        header_row = df.iloc[0]
        df2 = pd.DataFrame(df.values[1:], columns=header_row)

        # st.table(df2)
        	
        symbol_dict = df2.set_index('SYMBOL').to_dict()['NAME OF COMPANY']

        options = st.multiselect(
            'Stocks to track',
            list(symbol_dict.values()),
            [])

        st.write('You selected:', options)

        if st.button('Save'):
            print('options = ', options)
            # filtered_dict = dict(filter(lambda item: item[0] in options, symbol_dict)) 
            filtered_dict = dict(filter(lambda item: item[1] in options, symbol_dict.items())) 
            print('filtered_dict = ', filtered_dict)
            buy_tracker.add_stocks(filtered_dict)
            buy_tracker.save_list()
            st.write('Saved!')


app()
