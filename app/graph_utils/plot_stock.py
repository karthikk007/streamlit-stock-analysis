
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

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

    fig.update_xaxes(
        rangeslider_visible=True,
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
    )

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
                margin=dict(l=0, r=0, t=0, b=0, pad=0),
                legend=dict(
                    x=0,
                    y=0.99,
                    traceorder="normal",
                    font=dict(size=12),
                ),
                autosize=False,
            )
