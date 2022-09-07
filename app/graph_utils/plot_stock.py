import plotly.graph_objects as go

def plot_stock_close(fig, df, name):
    """
    Plot time-serie line chart of closing price on a given plotly.graph_objects.Figure object
    """
    fig = fig.add_trace(
        go.Scatter(
            x=df.date,
            y=df['Close'],
            mode="lines",
            name=name,
        )
    )

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
        )
    )

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

    return fig