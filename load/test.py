import pandas as pd
from datetime import datetime
import requests

from icalendar import Calendar

date1 = '20210523'
date2 = '20210710'

ics_url = 'https://www.officeholidays.com/ics-fed/usa'

df = {'Datetime_Start': pd.to_datetime([date1]),
      'Datetime_End': pd.to_datetime([date2])}
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
mydates = pd.date_range(date1, date2).tolist()
print(mydates)
for a in list(mydates):
    if pd.to_datetime(a) in holidays:
        # print(pd.to_datetime(a))
        mydates.remove(a)

excludeWeekend = pd.bdate_range(date1, date2)
print(excludeWeekend)
for a in list(mydates):
    print(pd.to_datetime(a))
    if pd.to_datetime(a) not in excludeWeekend:
        mydates.remove(a)
print(mydates)





