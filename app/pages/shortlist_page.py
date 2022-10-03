# Contents of ~/my_app/pages/page_2.py
import streamlit as st
from config.config import Tracker
from data_source.ticker import Ticker
import pandas as pd

def app():
    st.markdown("# Shortlist ❄️")
    st.sidebar.markdown("# Shortlist ❄️")

    ticker = Ticker()
    tracker = Tracker()

    with st.spinner('loading...'):
        ticker.load_ticker_list()

        df = pd.DataFrame(ticker.all_stock_codes.items())
        header_row = df.iloc[0]
        df2 = pd.DataFrame(df.values[1:], columns=header_row)

        # st.table(df2)
        	
        symbol_dict = df2.set_index('SYMBOL').to_dict()['NAME OF COMPANY']

        list_to_add = filter_tracked_list(symbol_dict, tracker.track_list)
        list_to_delete = filter_delete_list(symbol_dict, tracker.track_list)

        add_tab, delete_tab = st.tabs(["Select", "Delete"])

        with add_tab:
            add_add_tab_items(tracker, symbol_dict, list_to_add)

        with delete_tab:
            add_delete_tab_items(tracker, symbol_dict, list_to_delete)


def add_add_tab_items(tracker, symbol_dict, list_to_add):
    options = st.multiselect(
        'Stocks to track',
        list(list_to_add),
        [])

    st.write('You selected:', options)
    
    if st.button('Save'):
        # filtered_dict = dict(filter(lambda item: item[0] in options, symbol_dict)) 
        filtered_dict = dict(filter(lambda item: item[1] in options, symbol_dict.items())) 

        tracker.add_stocks(filtered_dict)
        tracker.save_list()
        st.write('Saved!')

    st.write('Track list:', tracker.track_list)


def add_delete_tab_items(tracker, symbol_dict, list_to_delete):
    options = st.multiselect(
        'Stocks to untrack',
        list(list_to_delete),
        [])

    st.write('You deleted:', options)
    
    if st.button('Delete'):
        # filtered_dict = dict(filter(lambda item: item[0] in options, symbol_dict)) 
        filtered_dict = dict(filter(lambda item: item[1] in options, symbol_dict.items())) 

        tracker.remove_stocks(filtered_dict)
        tracker.save_list()
        st.write('Deleted!')

    st.write('Track list:', tracker.track_list)


def filter_tracked_list(source_list, track_list):
    return list(filter(lambda x: x not in track_list.values(), source_list.values()))

def filter_delete_list(source_list, track_list):
    return track_list.values()

app()
