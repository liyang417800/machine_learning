# coding=gbk
import sys



def data_diff(begin_date,end_date): #2017-05-08 10:00:00   2017-05-10 14:00:00
    # detail = line.strip().split('\t')
    # if (len(detail) < 2):
    #     continue
    # begin_date = detail[0]
    # end_date = detail[1]



    trans_at_month = trans_at.split(',')
    if (len(trans_at_month) != 12):
        continue
    flag = True
    for money in trans_at_month:
        if (float(money) < 10000.0):
            flag = False
    if (flag):
        print '%s\t%s\t%s\t%s' % (mid, pid, trans_at, total_cnt)

