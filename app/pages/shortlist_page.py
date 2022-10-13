# Contents of ~/my_app/pages/page_2.py
import streamlit as st

import pandas as pd
from services.cache_handler.stock_tracker_handler import StockTrackingHandler

from services.data_fetcher.ticker_data_fetcher import TickerDataFetcher

def app():
    st.markdown("# Shortlist ❄️")
    st.sidebar.markdown("# Shortlist ❄️")

    ticker_data_fetcher = TickerDataFetcher()
    tracker = StockTrackingHandler.instance()

    with st.spinner('loading...'):
        ticker_data_fetcher.load_ticker_list()


        symbol_dict = ticker_data_fetcher.get_df_dict()

        list_to_add = filter_tracked_list(symbol_dict, tracker.track_list())
        list_to_delete = filter_delete_list(symbol_dict, tracker.track_list())

        add_tab, delete_tab = st.tabs(["Select", "Delete"])

        with add_tab:
            add_add_tab_items(tracker, symbol_dict, list_to_add)

        with delete_tab:
            add_delete_tab_items(tracker, symbol_dict, list_to_delete)


def add_add_tab_items(tracker: StockTrackingHandler, symbol_dict, list_to_add):
    options = st.multiselect(
        'Stocks to track',
        list(list_to_add),
        [])

    st.write('You selected:', options)
    
    if st.button('Save'):
        # filtered_dict = dict(filter(lambda item: item[0] in options, symbol_dict)) 
        filtered_dict = dict(filter(lambda item: item[1] in options, symbol_dict.items())) 

        tracker.add_stocks(filtered_dict)
        tracker.save()
        st.write('Saved!')

        st.experimental_rerun()

    st.write('Track list:', tracker.track_list())


def add_delete_tab_items(tracker: StockTrackingHandler, symbol_dict, list_to_delete):
    options = st.multiselect(
        'Stocks to untrack',
        list(list_to_delete),
        [])

    st.write('You deleted:', options)
    
    if st.button('Delete'):
        # filtered_dict = dict(filter(lambda item: item[0] in options, symbol_dict)) 
        filtered_dict = dict(filter(lambda item: item[1] in options, symbol_dict.items())) 

        tracker.remove_stocks(filtered_dict)
        tracker.save()
        st.write('Deleted!')

        st.experimental_rerun()

    st.write('Track list:', tracker.track_list())


def filter_tracked_list(source_list, track_list):
    return list(filter(lambda x: x not in track_list.values(), source_list.values()))

def filter_delete_list(source_list, track_list):
    return track_list.values()

app()
