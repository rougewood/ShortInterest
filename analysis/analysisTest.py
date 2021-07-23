from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import time
from datetime import timedelta
import datetime

# I added this code to get fake data, works wtihout tws running
from ibapi.common import BarData
from random import random

start = datetime.datetime.utcnow()


def fake_data(reqId, ib):
    last = reqId * 10
    for i in range(60, 0, -10):
        bar = BarData();
        bar.date = start - timedelta(minutes=i)
        last += random() - 0.5
        bar.close = last
        bar.volume = reqId * 1000
        ib.historicalData(reqId, bar)
    ib.historicalDataEnd(reqId, "", "")


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []

        # always include this for important messages, also turn on api logging in TWS/IBG

    def error(self, reqId, errorCode, errorString):
        print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

    def historicalData(self, reqId, bar):
        self.data.append([bar.date, bar.close, bar.volume, sym_dict[reqId]])

    # include this callback to track progress and maybe disconnectwhen all are finished
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("finished", sym_dict[reqId])


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# threading is needed only if you plan to interact after run is called
# this is a good way if you use a ui like jupyter
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# you should wait for nextValidId instead of sleeping, what if it takes more than 1 second?
time.sleep(1)

symbols = ['SPY', 'MSFT', 'GOOG', 'AAPL', 'QQQ', 'IWM', 'TSLA']

reqId = 1
sym_dict = {}
for sym in symbols:
    contract = Contract()
    contract.symbol = str(sym)
    sym_dict[reqId] = sym
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "ISLAND" # you may need this for msft
    app.reqHistoricalData(reqId, contract, "", "1 D", "10 mins", "ADJUSTED_LAST", 1, 2, False, [])
    # fake_data(reqId, app)
    reqId += 1
    # now you need to sleep(10) to make sure you don't get a pacing error for too many requests

# don't sleep, use historicalDataEnd to know when finished
time.sleep(5)

df = pd.DataFrame(app.data, columns=['DateTime', 'ADJUSTED_LAST', 'Volume', 'sym'])
df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s')

# make an index and sort
df = df.set_index(['sym', 'DateTime']).sort_index()
# now you can use the indexes
print(df.loc[("MSFT", "2021")])