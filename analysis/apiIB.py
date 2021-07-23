from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import pandas as pd
import datetime
import mplfinance as fplt
import xml.etree.ElementTree as ET
import threading

class MyWrapper(EWrapper):

    def __init__(self):
        self.df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    def historicalData(self, reqId:int, bar: BarData):
        #7 data is received for every bar
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        self.df.loc[len(self.df)] = [bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume]

    def fundamentalData(self, reqId: int, data: str):
        super().fundamentalData(reqId, data)
        print("FundamentalData Returned. ReqId: {}, XML Data: {}".format(
            reqId,  data))
        print(self.getFloatShares(ET.fromstring(data)))

    def getFloatShares(self, elem):
        # print(elem.tag)
        cap = 0.0
        price = 0.0
        for child in elem.findall('./Company/SecurityInfo/Security/MarketData/MarketDataItem'):
            # self.show(child)
            # print(child)
            # print(child.tag, child.attrib)
            attrList = child.items()
            print(len(attrList), " : [", attrList, "]")
            if child.attrib['type']=='MARKETCAP':
                cap = float(child.text)
            if child.attrib['type']=='CLPRICE':
                price = float(child.text)
        return int(cap/price)


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        #8 data is finished
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        #9 this is the logical end of your program
        print("finished")
        print(self.df)
        self.df.index = pd.DatetimeIndex(self.df['date'])
        fplt.plot(
            self.df,
            type='candle',
            style='charles',
            title='NIO',
            ylabel='Price ($)',
            volume=True,
            ylabel_lower='Shares\nTraded',
        )

    def error(self, reqId, errorCode, errorString):
        # these messages can come anytime.
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

def run_loop():
    app.run()

app = EClient(MyWrapper())
# 2 connect to TWS/IBG
app.connect("127.0.0.1", 7496, clientId=123)

# threading is needed only if you plan to interact after run is called
# this is a good way if you use a ui like jupyter
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

contract = Contract()
contract.secType = "STK"  # FUT
contract.symbol = "NIO"
contract.currency = "USD"
contract.exchange = "ISLAND"

# app.reqFundamentalData(1, contract, 'RESC', [])
app.reqHistoricalData(1, contract, "", "6 M", "1 day", "TRADES", 1, 2, False, [])