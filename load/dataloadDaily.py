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
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        print(start_date)
        d1 = start_date.strftime("%Y%m%d")
        base_path = Path(__file__).parent
        dest_path = '../data/' + d1 + '/'
        file_path = (base_path / dest_path).resolve()
        Path(file_path).mkdir(parents=True, exist_ok=True)
        os.chdir(file_path)
        for exchange in exchanges:
            load(exchange, d1, file_path)
        # changePath(start_date)
        mongoimport('CNMSshvol'+start_date.strftime("%Y%m%d")+'.txt', 'shortInterest', 'daily')
        start_date += delta
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
    data = pd.read_csv(csv_path, delimiter='|')
    payload = json.loads(data.to_json(orient='records'))
    coll.insert_many(payload)

loadAll(datetime.date(2021, 7, 6), datetime.date(2021, 7, 6))
# loadAll(datetime.date.today(), datetime.date.today())

# schedule.every().day.at("1:30").do(load)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)