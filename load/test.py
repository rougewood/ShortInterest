import pandas as pd
from datetime import datetime
import requests

from icalendar import Calendar







import pandas as pd
from pandas_datareader import data as web
from pandas_datareader import data
import plotly.graph_objects as go
import quandl

stock = 'AMC'

# df =quandl.get("WIKI/AAPL", start_date="2018-01-01", end_date="2018-07-01")
df = data.DataReader('AAPL', 'quandl', start='2021-01-01', end='2021-07-08')
#df = web.DataReader(stock, data_source='yahoo', start='01-01-2020')

candle = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': 'AMC',
    'showlegend': True
}
# Config graph layout
layout = go.Layout({
    'title': {
        'text': 'AAPL Moving Averages',
        'font': {
            'size': 15
        }
    }
})
fig = go.Figure(data=[candle])
fig.show()



