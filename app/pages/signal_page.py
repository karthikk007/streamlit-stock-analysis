# Contents of ~/my_app/pages/page_3.py
import streamlit as st


def app():
    st.markdown("# Signals 🎉")
    st.sidebar.markdown("# Signals 🎉")

    buy_signal_tab, sell_signal_tab = st.tabs(["Buy", "Sell"])

    with buy_signal_tab:
        add_buy_signal_tab_items()

    with sell_signal_tab:
        add_sell_signal_tab_items()


def add_buy_signal_tab_items():
    pass


def add_sell_signal_tab_items():
    pass


app()
