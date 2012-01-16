#!/usr/bin/python

import datetime

# Convert 2011-01-13 to two datetime objects with range of full day
def date_string_to_dayrange(date_string):
    (year, month, day) = map(lambda x: int(x), date_string.split('-'))

    dt_low  = datetime.datetime(year, month, day)
    dt_high = dt_low + datetime.timedelta(days=1, seconds=-1)

    return (dt_low, dt_high)

