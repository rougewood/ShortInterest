from ibapi import ibConnection, message
from ibapi.contract import Contract
from time import sleep

def fundamentalData_handler(msg):
    print(msg)

def error_handler(msg):
    print(msg)

tws = ibConnection("127.0.0.1",port=7496, clientId=997)
tws.register(error_handler, message.Error)
tws.register(fundamentalData_handler, message.fundamentalData)
tws.connect()

c = Contract()
c.m_symbol = 'MMM'
c.m_secType = 'STK'
c.m_exchange = "SMART"
c.m_currency = "USD"

tws.reqFundamentalData(1,c,'ReportsFinStatements')

sleep(2)

tws.disconnect()