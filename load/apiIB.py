from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import pandas as pd
import datetime
import mplfinance as fplt
import xml.etree.ElementTree as ET

class MyWrapper(EWrapper):

    def __init__(self):
        self.df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    def nextValidId(self, orderId:int):
        #4 first message received is this one
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #5 start requests here
        self.start()

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
        app.disconnect()
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

    def start(self):
        queryTime = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")

        fx = Contract()
        fx.secType = "STK" #FUT
        fx.symbol = "NIO"
        fx.currency = "USD"
        fx.exchange = "ISLAND"

        #6 request data, using fx since I don't have Japanese data
        # app.reqHistoricalData(4102, fx, queryTime,"1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        # app.reqHistoricalData(4102, fx, queryTime, "6 M", "1 day", "TRADES", 1, 1, False, [])
        app.reqFundamentalData(1, fx, 'RESC', [])

app = EClient(MyWrapper()) #1 create wrapper subclass and pass it to EClient
app.connect("127.0.0.1", 7496, clientId=124) #2 connect to TWS/IBG
app.run() #3 start message thread