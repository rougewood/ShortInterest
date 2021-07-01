import schedule
import time
from dataloadDaily import loadAll
import datetime

schedule.every().day.at("20:30").do(loadAll(datetime.now(), datetime.now()))

while 1:
    schedule.run_pending()
    time.sleep(1)