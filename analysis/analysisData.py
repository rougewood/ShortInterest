import datetime
import os
import csv
from pathlib import Path
import pandas as pd
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR

def loadShortedStockToDF( dest_date ):
    # today = datetime.date.today();
    # yesterday = today - datetime.timedelta(days=1)
    base_path = Path(__file__).parent
    dest_path = '../data/' + dest_date + '/'
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

# sortByShortVolume('20210624')
sortByShortVolume('20210706')
# sortByTotalVolume('20210702')

# def histShortInterest(stock, start_date, end_date):
#     mydates = pd.date_range(start_date, end_date).tolist()
#
#     return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))



