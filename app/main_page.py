# Contents of ~/my_app/main_page.py

import streamlit as st

from stock_data.stock import Stock
import datetime
from dateutil.relativedelta import relativedelta

APP_NAME = "Stock App!"

def app():
    st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
    st.sidebar.title = APP_NAME

    st.markdown("# 🎈 Stock forecast dashboard 📈")
    st.sidebar.markdown("# Main page 🎈")
    st.title('')
    
    show_date_picker()
    show_stock()
    

def show_date_picker():
    with st.sidebar.container():
        st.markdown("## Insights") # add a title to the sidebar container
        con1 = st.sidebar.container()
        show_date_range(con1)

        con2 = st.sidebar.container()

        col1, col2 = con2.columns(2)

        end_date = datetime.datetime.today()
        start_date = end_date - relativedelta(years=5)
        min_date = end_date - relativedelta(years=20)

        col1.date_input('From', start_date, min_date, end_date, key='from_date_picker', on_change=did_change_date_picker)
        col2.date_input('To', end_date, min_date, end_date, key='to_date_picker', on_change=did_change_date_picker)

        
def show_date_range(container):
    container.selectbox('Range', ('-', '3 Months', '6 Months', '1 Year', '2 Years', '3 Years', '4 Years', '5 Years', '10 Years', 'Max'), index=7, key='range_picker', on_change=did_change_date_range)


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


def show_stock():
    from_date_picker = st.session_state['from_date_picker']
    to_date_picker = st.session_state['to_date_picker']

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
    stock = Stock(symbol='TCS.NS', start=start, end=end)
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
        st.write(stock.data)

app()


