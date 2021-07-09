from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override()
import pandas as pd
from dateutil.relativedelta import relativedelta

files=[]
today = date.today()
six_month_ago = date.today() + relativedelta(months=-6)
def loadTickHist(tickers):
    for ticker in tickers:
        data = pdr.get_data_yahoo(ticker, start=six_month_ago, end=today)
        dataname = ticker +'_'+str(today)
        files.append(dataname)
        SaveData(data, dataname)

# Create a data_short folder in your current dir.
def SaveData(df, filename):
    df.to_csv('./data_hist/'+filename+'.csv')

for i in range(0, 11):
    df1 = pd.read_csv('./data_hist/'+ str(files[i]) +'.csv')
    print(df1.head())


