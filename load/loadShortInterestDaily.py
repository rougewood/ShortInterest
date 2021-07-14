import os

import schedule
import time
import requests
import datetime
from datetime import date
from pathlib import Path
from pymongo import MongoClient
import json
import pandas as pd

from icalendar import Calendar

finraSite = 'http://regsho.finra.org/'


def load(exchange, file_date, file_path):
    print("I'm loading for " + exchange + " ...")
    file_name = get_file_name(exchange, file_date)
    url = finraSite+file_name
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)


def get_file_name(file, file_date):
    return file+file_date+'.txt'

def loadToday():
    loadAll(datetime.date.today(), datetime.date.today())

def loadAll(start_date, end_date):
    # clearMongoDB('shortInterest', 'daily')

    exchanges = ["CNMSshvol","FNQCshvol","FNRAshvol","FNSQshvol","FNYXshvol","FORFshvol"]
    # start_date = datetime.date(2021, 1, 1)
    # end_date = datetime.date(2021, 6, 4)
    dateList = getDateList(start_date, end_date)
    for start_date in dateList:
        print(start_date)
        # d1 = start_date.strftime("%Y%m%d")
        base_path = Path(__file__).parent
        dest_path = '../data_short/' + start_date + '/'
        file_path = (base_path / dest_path).resolve()
        Path(file_path).mkdir(parents=True, exist_ok=True)
        os.chdir(file_path)
        for exchange in exchanges:
            load(exchange, start_date, file_path)
        # changePath(start_date)
        mongoimport('CNMSshvol'+start_date+'.txt', 'shortInterest', 'daily')

# pd.date_range('2011-01-05', '2011-01-09', freq=BDay())

def clearMongoDB(db_name, coll_name, db_url='localhost', db_port=27017):
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    coll.delete_many({})

def mongoimport(csv_path, db_name, coll_name, db_url='localhost', db_port=27017):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    data = pd.read_csv(csv_path, delimiter='|').query('ShortVolume > 0')
    payload = json.loads(data.to_json(orient='records'))
    coll.insert_many(payload)

def getDateList(start_date,end_date):
    ics_url = 'https://www.officeholidays.com/ics-fed/usa'

    df = {'Datetime_Start': pd.to_datetime([start_date]),
          'Datetime_End': pd.to_datetime([end_date])}
    df = pd.DataFrame(df)

    df['days_in_range'] = df.apply(
        lambda x: pd.date_range(x['Datetime_Start'], x['Datetime_End']),
        axis=1)

    # remove weekends
    df['days_in_range'] = df['days_in_range'].apply(lambda x: x[x.dayofweek <= 4])

    # remove holidays
    calendar = Calendar.from_ical(requests.get(ics_url).content)
    holidays = [pd.to_datetime(x['DTSTART'].dt).date()
                for x in calendar.walk('VEVENT')]
    print(holidays)
    # print(calendar)
    #
    mydates = pd.date_range(start_date, end_date).tolist()
    print(mydates)
    for a in list(mydates):
        if pd.to_datetime(a) in holidays:
            # print(pd.to_datetime(a))
            mydates.remove(a)

    excludeWeekend = pd.bdate_range(start_date, end_date)
    # print(excludeWeekend)
    for a in list(mydates):
        print(pd.to_datetime(a))
        if pd.to_datetime(a) not in excludeWeekend:
            mydates.remove(a)

    return [x.strftime('%Y%m%d') for x in list(mydates)]


loadAll(datetime.date(2021, 6, 10), datetime.date(2021, 7, 9))
# loadAll(datetime.date.today(), datetime.date.today())

# schedule.every().day.at("1:30").do(load)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

