# coding=gbk
import sys
import time

# workday = {'2017-05-08′:'0', 'ob2′:'mouse', 'ob3′:'printer'}



def data_diff(begin_date,end_date): #2017-05-08 10:00:00   2017-05-10 14:00:00
    # detail = line.strip().split('\t')
    # if (len(detail) < 2):
    #     continue
    # begin_date = detail[0]
    # end_date = detail[1]
    t1 = time.mktime(time.strptime(end_date, "%Y-%m-%d %H:%M:%S"))
    t2 = time.mktime(time.strptime(begin_date, "%Y-%m-%d %H:%M:%S"))
    delta = (t1 - t2)/3600

    # trans_at_month = trans_at.split(',')
    # if (len(trans_at_month) != 12):
    #     continue
    # flag = True
    # for money in trans_at_month:
    #     if (float(money) < 10000.0):
    #         flag = False
    # if (flag):
    #     print '%s\t%s\t%s\t%s' % (mid, pid, trans_at, total_cnt)
    print delta

if __name__=='__main__':
    data_diff('2017-05-08 10:00:00','2017-05-10 14:00:00')
