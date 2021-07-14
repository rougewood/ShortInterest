import datetime
import os
import csv
from pathlib import Path
import pandas as pd
import pymongo



def loadFromMongoDB(symbol):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["shortInterest"]
    mycol = mydb["daily"]

    myquery = {"Symbol": symbol}
    mydoc = mycol.find(myquery)

    for x in mydoc:
        print(x)

def loadShortedStockToDF( dest_date ):
    # today = datetime.date.today();
    # yesterday = today - datetime.timedelta(days=1)
    base_path = Path(__file__).parent
    dest_path = '../data_short/' + dest_date + '/'
    file_path = (base_path / dest_path).resolve()
    os.chdir(file_path)

    # with open('CNMSshvol'+dest_date+'.txt', 'r') as f:
    #     first_column = [row[0] for row in csv.reader(f, delimiter='|')]
    #     print(first_column[1:])
    df = pd.read_csv('CNMSshvol'+dest_date+'.txt', delimiter='|')
    df["ShortRatio"] = df["ShortVolume"]/df["TotalVolume"]

    return df

def sortByShortVolume(dest_date):
    df = loadShortedStockToDF( dest_date )
    final_df = df.sort_values(by=['ShortVolume'], ascending=False)
    print(final_df[:50])

def sortByTotalVolume(dest_date):
    df = loadShortedStockToDF( dest_date )
    final_df = df.sort_values(by=['TotalVolume'], ascending=False)
    print(final_df[:20])

# def tickerChart():
#     app = EClient(MyWrapper())  # 1 create wrapper subclass and pass it to EClient
#     app.connect("127.0.0.1", 7496, clientId=123)  # 2 connect to TWS/IBG
#     app.run()  # 3 start message thread

def sortByShortRatio(dest_date):
    df = loadShortedStockToDF( dest_date )
    final_df = df.sort_values(by=['ShortRatio'], ascending=False).query('ShortVolume>1000000')
    print(final_df[:100])

def sortByShortRatio(dest_date, symbol):
    df = loadShortedStockToDF( dest_date )
    final_df = df.sort_values(by=['ShortRatio'], ascending=False).query('ShortVolume>1000000')
    final_df = final_df.loc[final_df['Symbol']==symbol]
    print(final_df[:20])

# sortByShortVolume('20210624')
# sortByShortVolume('20210706')
# loadFromMongoDB('NIO')
sortByTotalVolume('20210709')
# sortByShortRatio('20210707', 'CARV')





