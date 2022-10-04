# Contents of ~/my_app/main_page.py

from operator import index
from select import select
import streamlit as st
from stock_handler.stock import StockTickerData
from stock_handler.stock import StockData
from config.config import Tracker
from stock_handler.stock import Stock
import datetime
from dateutil.relativedelta import relativedelta

APP_NAME = "Stock App!"
USING_DEFAULT_LIST = True

def app():
    st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
    st.sidebar.title = APP_NAME

    st.markdown("# 🎈 Stock forecast dashboard 📈")
    st.sidebar.markdown("# Main page 🎈")
    st.title('')
    
    show_ticker_selector()
    show_date_picker()

    technical_analysis_tab, fundamental_analysis_tab = st.tabs(["Technical Analysis", "Fundamental Analysis"])

    with technical_analysis_tab:
        show_stock()

    with fundamental_analysis_tab:
        show_fundamentals()

    
    
def show_ticker_selector():
    global USING_DEFAULT_LIST

    track_list = get_track_list()

    # List of tickers
    TICKERS = ['TCS.NS', 'ITC.NS', 'RELIANCE.NS', 'COALINDIA.NS', 'VINATIORGA.NS', 'PAGEIND.NS', 'DEEPAKNTR.NS', 'ZOMATO.NS', 'AMARAJABAT.NS']

    if len(track_list.values()) > 0:
        USING_DEFAULT_LIST = False
        TICKERS = track_list.values()

    select_index = 0

    # Select ticker
    st.sidebar.selectbox('Select ticker', sorted(TICKERS), index=select_index, key='ticker')

def show_date_picker():
    with st.sidebar.container():
        st.markdown("## Insights") # add a title to the sidebar container
        con1 = st.sidebar.container()
        show_date_range(con1)

        con2 = st.sidebar.container()

        col1, col2 = con2.columns(2)

        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=1)
        min_date = end_date - relativedelta(years=20)

        col1.date_input('From', start_date, min_date, end_date, key='from_date_picker', on_change=did_change_date_picker)
        col2.date_input('To', end_date, min_date, end_date, key='to_date_picker', on_change=did_change_date_picker)

        
def show_date_range(container):
    periods = [
        "1d", 
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]
    container.selectbox('Range', ('-', '3 Months', '6 Months', '1 Year', '2 Years', '3 Years', '4 Years', '5 Years', '10 Years', 'Max'), index=3, key='range_picker', on_change=did_change_date_range)


def did_change_date_picker():
    print("did_change_date_picker")

def did_change_date_range():
    val = st.session_state['range_picker']

    end_date = datetime.datetime.today()
    months = 0

    if val == '-':
        months = 1
    elif val == '3 Months':
        months = 3
    elif val == '6 Months':
        months = 6
    elif val == '1 Year':
        months = 12
    elif val == '2 Years':
        months = 24
    elif val == '3 Years':
        months = 36
    elif val == '4 Years':
        months = 48
    elif val == '5 Years':
        months = 60
    elif val == '10 Years':
        months = 120
    elif val == 'Max':
        months = 240

    if months == 1:
        start_date = end_date - relativedelta(weeks=3)
    elif months >= 12:
        start_date = end_date - relativedelta(years=int(months/12))
    else: 
        start_date = end_date - relativedelta(months=months)

    st.session_state['from_date_picker'] = start_date
    st.session_state['to_date_picker'] = end_date


def show_fundamentals():
    st.write('Fundamental analysis')


def show_stock():
    global USING_DEFAULT_LIST

    from_date_picker = st.session_state['from_date_picker']
    to_date_picker = st.session_state['to_date_picker']
    range_key = st.session_state['range_picker']

    ticker = st.session_state['ticker']

    if not USING_DEFAULT_LIST:
        track_list = get_track_list()
        index = list(track_list.values()).index(ticker)
        ticker = list(track_list.keys())[index]     

    start = datetime.datetime(
        year=from_date_picker.year,
        month=from_date_picker.month,
        day=from_date_picker.day
    ) 
    end = datetime.datetime(
        year=to_date_picker.year,
        month=to_date_picker.month,
        day=to_date_picker.day
    ) 

    # stock = Stock(symbol='ITC.NS', start=start, end=end)
    ticker_data = StockTickerData(ticker, track_list[ticker])
    print("ticker = ", ticker)
    stock_data = StockData(ticker=ticker_data, key=range_key, start=start, end=end)
    stock = Stock(stock_data)
    # stock = Stock(symbol='RELIANCE.NS', start=start, end=end)

    with st.spinner('Loading data...'):
        stock.load_data()
    st.success('Data Loaded.')

    # # # ------------------------Plot stock linechart--------------------
    fig = stock.plot_raw_data()

    st.plotly_chart(fig, use_container_width=True)

    change_c = st.sidebar.container()
    with change_c:
        stock.show_delta()

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(stock.stock_data.data)

def get_track_list():
    tracker = Tracker()
    track_list = tracker.track_list

    return track_list


app()


