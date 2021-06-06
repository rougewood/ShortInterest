import datetime
import os
import csv
from pathlib import Path
import pandas as pd

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
    print(final_df.head(10))

def sortByTotalVolume(dest_date):
    df = loadShortedStockToDF( dest_date )
    final_df = df.sort_values(by=['TotalVolume'], ascending=False)
    print(final_df.head(10))


sortByShortVolume('20210603')
sortByTotalVolume('20210604')
