# Contents of ~/my_app/pages/page_2.py
import streamlit as st
from data_source.ticker import Ticker
import pandas as pd

def app():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

    ticker = Ticker()

    with st.spinner('loading...'):
        ticker.load_ticker_list()

        df = pd.DataFrame(ticker.all_stock_codes.items())
        header_row = df.iloc[0]
        df2 = pd.DataFrame(df.values[1:], columns=header_row)

        # st.table(df2)
        	
        dict = df2.set_index('SYMBOL').to_dict()['NAME OF COMPANY']
        print(dict.values())


        options = st.multiselect(
            'Stocks to track',
            list(dict.values()),
            [])

        st.write('You selected:', options)


app()
