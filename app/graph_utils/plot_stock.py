
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

UP_COLOR = '#ff9900'
DOWN_COLOR = 'black'

def plot_macd(fig, df, name):

    # https://www.alpharithms.com/calculate-macd-python-272222/
    # Calculate MACD values using the pandas_ta library
    length = 8
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    df.ta.rsi(close='close', length=length, append=True, signal_indicators=True, xa=60, xb=40, drift=3)

    # Add indicators, using data from before
    df.ta.sma(close='volume', length=50, append=True)

    # Add some indicators
    df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    
    # View result
    pd.set_option("display.max_columns", None)  # show all columns

    # Force lowercase (optional)
    df.columns = [x.lower() for x in df.columns]

    color_volume(df)

    # print(df)

    df = df.set_index('datetime')

    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=5, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.025,
            row_width=[0.15, 0.15, 0.15, 0.15, 0.5],
            subplot_titles=("Candle", 'Volume', "MACD", 'RSI'),
            # specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]]
        )

    # price Line
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['close'],
            line=dict(color='#38BEC9', width=2),
            name='close',
            # showlegend=False,
            legendgroup='1',
        ), row=1, col=1,
    )

    # Candlestick chart for pricing
    fig.append_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            # showlegend=False,
            # legendgroup='1',
            visible='legendonly',
            name='candle',
        ), row=1, col=1
    )

    # Volume
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['volume'],
            name='volume',
            # showlegend=False,
            # legendgroup='1',
            marker={'color':df['color']}
        ), row=2, col=1, 
    )

    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['sma_50'],
            name='vol_sma_50',
            # showlegend=False,
            # legendgroup='1',
            line=dict(color='red', width=2),
        ), row=2, col=1, 
    )


    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['macd_12_26_9'],
            line=dict(color='#ff9900', width=2),
            name='macd',
            # showlegend=False,
            legendgroup='2',
        ), row=3, col=1
    )
    
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['macds_12_26_9'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=3, col=1
    )

    # Colorize the histogram values
    colors = np.where(df['macdh_12_26_9'] < 0, '#000', '#ff9900')

    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['macdh_12_26_9'],
            name='histogram',
            marker_color=colors,
        ), row=3, col=1
    )

    rsi_col = 'rsi_' + str(length)
    # Make RSI Plot
    fig.add_trace(go.Scatter(
            x=df.index,
            y=df[rsi_col],
            line=dict(color='#ff9900', width=2),
            showlegend=False,
        ), row=4, col=1
    )

    # Add upper/lower bounds
    fig.update_yaxes(range=[-10, 110], row=4, col=1)
    fig.add_hline(y=0, col=1, row=4, line_color="#666", line_width=1)
    fig.add_hline(y=100, col=1, row=4, line_color="#666", line_width=1)

    # Add overbought/oversold
    fig.add_hline(y=30, col=1, row=4, line_color='#336699', line_width=1, line_dash='dash')
    fig.add_hline(y=70, col=1, row=4, line_color='#336699', line_width=1, line_dash='dash')


    # stoch Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['stochk_14_3_3'],
            line=dict(color='#ff9900', width=2),
            name='fast',
        ), row=5, col=1 
    )
    # stoch Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['stochd_14_3_3'],
            line=dict(color='#000000', width=2),
            name='slow'
        ), row=5, col=1  
    )

    # Extend our y-axis a bit
    fig.update_yaxes(range=[-10, 110], row=5, col=1)
    # Add upper/lower bounds
    fig.add_hline(y=0, col=1, row=5, line_color="#666", line_width=1)
    fig.add_hline(y=100, col=1, row=5, line_color="#666", line_width=1)
    # Add overbought/oversold
    fig.add_hline(y=20, col=1, row=5, line_color='#336699', line_width=1, line_dash='dash')
    fig.add_hline(y=80, col=1, row=5, line_color='#336699', line_width=1, line_dash='dash')


    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=12,
    )

    # adjust xaxis for rangebreaks
    dt_breaks = get_date_breaks(df)
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)],)

    # Update options and show plot
    fig.update_layout(layout)

    add_axis_steps(fig)
    show_spikes(fig)

    update_styling(fig)
    
    return fig


def plot_stock_close(fig, df, name):
    """
    Plot time-serie line chart of closing price on a given plotly.graph_objects.Figure object
    """
    line = go.Scatter(
            x=df.date,
            y=df['Close'],
            mode="lines",
            name=name,
        )

    fig.add_trace(line)
    add_axis_steps(fig)

    dt_breaks = get_date_breaks(df)

    # adjust xaxis for rangebreaks
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)] )

    update_styling(fig)

    return fig

def get_date_breaks(df):
    # grab first and last observations from df.date and make a continuous date range from that
    dt_all = pd.date_range(start=df['date'].iloc[0],end=df['date'].iloc[-1], freq = 'D')

    # check which dates from your source that also accur in the continuous date range
    dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in df['date']]

    # isolate missing timestamps
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]

    return dt_breaks

def update_styling(fig):
    #---------------styling for plotly-------------------------
    fig.update_layout(
                width=1200,
                height=800,
                margin=dict(l=20, r=20, t=20, b=20, pad=0),
                legend=dict(
                    x=0.01,
                    y=0.99,
                    traceorder="normal",
                    font=dict(size=12),
                    orientation="h"
                ),
                autosize=False,
                # paper_bgcolor="#5f7787",
                # plot_bgcolor="#99adba",
            )

def add_axis_steps(fig):

    fig.update_layout(
        xaxis = dict(
            rangeslider=dict(
                visible=False,
            ),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=9, label="9m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=2, label="2y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(count=4, label="4y", step="year", stepmode="backward"),
                    dict(count=5, label="5y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            autorange=True,
        ),
        # yaxis = dict(
        #     fixedrange = False,
        #     side='left'
        # ),
        # yaxis2 = dict(
        #     overlaying='y',
        #     side='right',
        #     anchor= 'x',
        # )
    )

    # fig.update_xaxes(
    #     rangeslider_visible=True,
    #     rangeselector=dict(
    #         buttons=list([
    #             dict(count=1, label="YTD", step="year", stepmode="todate"),
    #             dict(count=1, label="1m", step="month", stepmode="backward"),
    #             dict(count=3, label="3m", step="month", stepmode="backward"),
    #             dict(count=6, label="6m", step="month", stepmode="backward"),
    #             dict(count=9, label="9m", step="month", stepmode="backward"),
    #             dict(count=1, label="1y", step="year", stepmode="backward"),
    #             dict(count=2, label="2y", step="year", stepmode="backward"),
    #             dict(count=3, label="3y", step="year", stepmode="backward"),
    #             dict(count=4, label="4y", step="year", stepmode="backward"),
    #             dict(count=5, label="5y", step="year", stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     ),
    # )

def show_spikes(fig):

    fig.update_yaxes(spikethickness=1,
                 showspikes=True, spikemode='across', showline=False, spikedash='dash')

    fig.update_xaxes(spikethickness=1,
                 showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='dash')

    fig.update_layout(spikedistance=100, hoverdistance=20)

def color_volume(df):
    df['diff'] = df['close'] - df['open']
    df.loc[df['diff']>=0, 'color'] = UP_COLOR
    df.loc[df['diff']<0, 'color'] = DOWN_COLOR
