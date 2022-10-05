# Contents of ~/my_app/pages/page_3.py
import streamlit as st

from config.stock_tracker import StockTracker

from stock_handler.stock_signals import StockSignals



def app():
    st.markdown("# Signals 🎉")
    st.sidebar.markdown("# Signals 🎉")

    buy_signal_tab, sell_signal_tab = st.tabs(["Buy", "Sell"])

    stockSignals = StockSignals()

    with buy_signal_tab:
        add_buy_signal_tab_items(stockSignals)

    with sell_signal_tab:
        add_sell_signal_tab_items(stockSignals)


def add_buy_signal_tab_items(stockSignals: StockSignals):
    stockSignals.process_records()
    st.json(stockSignals.buy_signals)
    


def add_sell_signal_tab_items(stockSignals: StockSignals):
    stockSignals.process_records()
    st.json(stockSignals.sell_signals)



app()
