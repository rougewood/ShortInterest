import os

import schedule
import time
import requests
import datetime
from datetime import date
from pathlib import Path

finraSite = 'http://regsho.finra.org/'


def load( exchange, file_date, file_path):
    print("I'm loading for " + exchange + " ...")
    file_name = get_file_name(exchange, file_date)
    url = finraSite+file_name
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)


def get_file_name(file, file_date):
    return file+file_date+'.txt'


def loadAll():
    exchanges = ["CNMSshvol","FNQCshvol","FNRAshvol","FNSQshvol","FNYXshvol","FORFshvol"]
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2021, 6, 4)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        print(start_date)
        start_date += delta
        d1 = start_date.strftime("%Y%m%d")
        base_path = Path(__file__).parent
        dest_path = '../data/' + d1 + '/'
        file_path = (base_path / dest_path).resolve()
        Path(file_path).mkdir(parents=True, exist_ok=True)
        os.chdir(file_path)
        for exchange in exchanges:
            load(exchange, d1, file_path)

# pd.date_range('2011-01-05', '2011-01-09', freq=BDay())

loadAll()
# schedule.every().day.at("1:30").do(load)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)