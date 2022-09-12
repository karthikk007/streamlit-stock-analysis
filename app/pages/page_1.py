# Contents of ~/my_app/pages/page_2.py
import streamlit as st
from data_source.ticker import Ticker

def app():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

    ticker = Ticker()

    with st.spinner('loading...'):
        ticker.load_ticker_list()
        st.write(ticker.all_stock_codes)


app()
