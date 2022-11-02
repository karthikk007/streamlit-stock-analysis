# Contents of ~/my_app/main_page.py

from operator import index
import streamlit as st
import datetime

from dateutil.relativedelta import relativedelta
from services.cache.app_state_cache import AppStateCache

from services.cache_handler.stock_tracker_handler import StockTrackingHandler
from data_models.stock_data_view_model import StockDataViewModel
from data_models.ticker_data_model import TickerDataModel
from data_processor.stock_data_processor import StockDataProcessor


APP_NAME = "Stock App!"
USING_DEFAULT_LIST = True

st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
st.sidebar.title = APP_NAME

app_state = AppStateCache()

def app():
    # st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
    # st.sidebar.title = APP_NAME

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

    selected_ticker = None
    TICKERS = get_tickers()

    key = 'main_ticker_index'
    if key in app_state.cache:
        selected_ticker = app_state.cache[key]

    select_index = 0

    try:
        if selected_ticker:
            select_index = TICKERS.index(selected_ticker)
    except Exception as e:
        print(e)

    print('fallback: select_index = ', select_index)

    # Select ticker
    st.sidebar.selectbox('Select ticker', TICKERS, index=select_index, key='ticker', on_change=did_change_ticker)


def get_tickers():
    global USING_DEFAULT_LIST

    track_list = get_track_list()

    # List of tickers
    TICKERS = ['TCS', 'ITC', 'RELIANCE', 'COALINDIA', 'VINATIORGA', 'PAGEIND', 'DEEPAKNTR', 'ZOMATO', 'AMARAJABAT']

    if len(track_list.values()) > 0:
        USING_DEFAULT_LIST = False
        TICKERS = list(track_list.values())

    TICKERS = sorted(TICKERS)

    # keys = list(filter(lambda x: x not in track_list.keys(), source_list.keys()))
    # values = list(map(lambda x: '{} ({})'.format(source_list[x], x), keys))
    return TICKERS

def did_change_ticker():
    app_state.cache['main_ticker_index'] = st.session_state['ticker']
    app_state.save_cache()

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

    track_list = {}

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
    name = track_list[ticker] if len(track_list) > 0 else ''
    ticker_data = TickerDataModel(ticker, name)
    stock_data = StockDataViewModel(ticker=ticker_data, key=range_key, start=start, end=end)
    stock = StockDataProcessor(stock_data)
    # stock = Stock(symbol='RELIANCE.NS', start=start, end=end)

    with st.spinner('Loading data...'):
        try:
            stock.load_data()
        except Exception as e:
            raise e

    if len(stock.stock_data.data) < 30:
        st.write('{} has {} only entries...'.format(ticker, len(stock.stock_data.data)))

        e = RuntimeError('{} has {} only entries...'.format(ticker, len(stock.stock_data.data)))
        st.exception(e)
        
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
    tracker = StockTrackingHandler.instance()
    track_list = tracker.track_list()

    return track_list


app()


