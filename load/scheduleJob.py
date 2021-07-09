import schedule
import time
from loadShortInterestDaily import loadToday
import datetime

# schedule.every().day.at("20:30").do(loadAll(datetime.date.today(), datetime.date.today()))

def job():
    print("I'm working...")

schedule.every().day.at("20:30").do(loadToday)

while 1:
    schedule.run_pending()
    time.sleep(1)