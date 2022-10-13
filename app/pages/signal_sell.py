# Contents of ~/my_app/pages/page_3.py
import streamlit as st
import pandas as pd

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from interactor.stock_interactor import get_market_capital_category
from services.cache_handler.snooze_tracker_handler import SnoozeTrackerHandler
from services.cache.app_state_cache import AppStateCache

from data_processor.stock_signals_processor import StockSignalProcessor, StockSignalsData


snooze_handler = SnoozeTrackerHandler()


APP_NAME = "Stock App!"
st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
st.sidebar.title = APP_NAME

app_state = AppStateCache()

def app():
    if st.button('Refresh Table'):
        st.write('Table refreshed!!!')

        st.experimental_rerun()

    st.markdown("# Signals SELL 🎉")
    st.sidebar.markdown("# Signals SELL 🎉")
    

    with st.sidebar:
        add_categories()

    with st.spinner('Loading data...'):
        category = st.session_state['category_list']

        stockSignals = StockSignalProcessor()
        stockSignals.process_records(category)

        add_sell_signal_tab_items(stockSignals)

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(stockSignals.get_stock_list(category))



def add_buy_signal_tab_items(stockSignals: StockSignalProcessor):
    add_selection_table(stockSignals.buy_signals, 'buy_signal_table')


def add_sell_signal_tab_items(stockSignals: StockSignalProcessor):
    add_selection_table(stockSignals.sell_signals, 'sell_signal_table')


def add_categories():
    category_list = get_market_capital_category()
    category_list = sorted(category_list)

    category = 'CAT-00'
    key = 'signal_sell_category'
    if key in app_state.cache:
        category = app_state.cache[key]

    st.session_state['category_list'] = category

    index = category_list.index(category)

    st.sidebar.selectbox('Select Category', sorted(category_list), index=index, key='category_list', on_change=did_change_category)


def did_change_category():
    category = st.session_state['category_list']

    app_state.cache['signal_sell_category'] = category
    app_state.save_cache()

    print('did_change_category category', category)

    st.write(category)


def add_selection_table(signals, key):

    signal_data = []

    snooze_list = snooze_handler.get_snooze_list()

    for (key, value) in signals.items():
        data = {}
        value: StockSignalsData = value

        ticker = value.get_ticker()

        data['ticker'] = ticker.symbol
        data['name'] = ticker.name
        data['Market Cap'] = value.screening_data['Market Cap']
        data['Close Price'] = value.screening_data['Close Price']
        data['SCORE'] = value.screening_data['SCORE']

        if key not in snooze_list:
            signal_data.append(data)

    if len(signal_data) == 0:
        data = {}
        data['ticker'] = ''
        data['name'] = ''

        signal_data.append(data)
    
    df = pd.DataFrame.from_dict(signal_data)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gd.configure_auto_height(True)
    gd.configure_pagination(True, True, 20)
    gridoptions = gd.build()

    grid_table = AgGrid(df, gridOptions=gridoptions,
        update_mode=GridUpdateMode.MANUAL, key=key, reload_data=True)
        

    st.write('## Selected')
    selected_rows = grid_table["selected_rows"]
    st.dataframe(selected_rows)

    perform_snooze(selected_rows)


def perform_snooze(selected_rows):

    filtered_list = list(map(lambda item: item['ticker'], selected_rows))

    if len(filtered_list) > 0:
        snooze_handler.snooze_list(filtered_list)


app()
