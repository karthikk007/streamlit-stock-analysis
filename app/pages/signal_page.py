# Contents of ~/my_app/pages/page_3.py
import streamlit as st
import pandas as pd

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from data_processor.stock_signals_processor import StockSignalProcessor, StockSignalsData




def app():
    st.markdown("# Signals 🎉")
    st.sidebar.markdown("# Signals 🎉")

    buy_signal_tab, sell_signal_tab = st.tabs(["Buy", "Sell"])

    stockSignals = StockSignalProcessor()

    with st.spinner('Loading data...'):
        with buy_signal_tab:
            add_buy_signal_tab_items(stockSignals)

        with sell_signal_tab:
            add_sell_signal_tab_items(stockSignals)


def add_buy_signal_tab_items(stockSignals: StockSignalsData):
    stockSignals.process_records()
    # st.json(stockSignals.buy_signals)
    add_selection_table(stockSignals.buy_signals, 'buy_signal_table')


def add_sell_signal_tab_items(stockSignals: StockSignalsData):
    stockSignals.process_records()
    # st.json(stockSignals.sell_signals)
    add_selection_table(stockSignals.sell_signals, 'sell_signal_table')


def add_selection_table(signals, key):
    signal_data = []

    data = {}
    data['ticker'] = ''
    data['name'] = ''

    signal_data.append(data)

    for (key, value) in signals.items():
        data = {}
        value: StockSignalsData = value

        ticker = value.get_ticker()

        data['ticker'] = ticker.symbol
        data['name'] = ticker.name

        signal_data.append(data)
    
    df = pd.DataFrame.from_dict(signal_data)
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED, key=key)


    if st.button('Snooze', key=key + 'button'):

        st.write('Snoozed!!!')

        st.experimental_rerun()

        

    st.write('## Selected')
    selected_row = grid_table["selected_rows"]
    st.dataframe(selected_row)


    # st.write(selected_row[0].keys())


app()
