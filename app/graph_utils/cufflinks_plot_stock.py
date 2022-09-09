import cufflinks as cf
from .plot_stock import get_date_breaks


def cf_plot_candlestick(df, ticker):
    # Interactive data visualizations using cufflinks
    # Create candlestick chart 
    df = df.set_index('datetime')
    qf = cf.QuantFig(df, legend='top', name=ticker, up_color= 'darkolivegreen', down_color='darkred')


    # Add Bollinger Bands (BOLL) study to QuantFigure.studies
    qf.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)

    # Add 'volume' study to QuantFigure.studies
    qf.add_volume()
    # qf.add_volume(up_color= 'darkolivegreen', down_color='darkred') 

    # Technical Analysis Studies can be added on demand
    # Add Relative Strength Indicator (RSI) study to QuantFigure.studies
    # qf.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
    qf.add_rsi(periods=14,color='java', legendgroup=True)

    qf.add_macd(signal_period=14)

    fig = qf.iplot(asFigure=True, dimensions=(1200, 1200))

    # adjust xaxis for rangebreaks
    dt_breaks = get_date_breaks(df)
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)] )

    return fig