# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time

import datetime
import sys

def data_month(data_day):

    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

if __name__=='__main__':
    print data_diff('2017-05-06 10:00:00','2017-05-07 14:00:00')