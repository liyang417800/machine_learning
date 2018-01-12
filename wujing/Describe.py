#encoding=utf-8
import csv
import scipy.stats as stats
import argparse
import pandas as pd
import time

#读取参数
parser = argparse.ArgumentParser()
parser.add_argument('--data_name',type=str,default='E:\data\d_train_20180102.csv',help='training data in csv format')
parser.add_argument('--savename',type=str,default='E:\data\c_train_des.csv',help='training data in csv format')
args = parser.parse_args()

def load_data(path):
    return pd.read_csv(path, error_bad_lines=False)   #读取CSV（逗号分割）文件到DataFrame

def des(data):
    decrib = ['feature', 'count', 'min', 'max', 'mean', '方差', '偏度', '峰度',
              '25%', '50%', '75%', '90%', '99.7%', '99.97%所占人数', '覆盖率', '划分（针对离散型变量）"	含义	"连续1:离散：0', 'meaning']
    savename=args.savename
    file0 = open(savename, 'wb+')  # 'wb'  wb+ 以二进制读写模式打开 (参见 w+ )
    output = csv.writer(file0, dialect='excel')
    output.writerow(decrib)
    total = len(data)
    fea_list = data.columns

    for m in range(1, len(fea_list)):
        try:
            colom = fea_list[m]
            print colom
            data_notnull = data[-data[colom].isnull()][colom]
            #print len(data_notnull)
            g_dist = sorted(data_notnull)
            lenth = len(g_dist)
            print lenth
            info = stats.describe(data_notnull)
            listdes = [colom, str(info[0]), str(info[1][0]), str(info[1][1]), str(info[2]),
                       str(info[3]), str(info[4]), str(info[5]), g_dist[int(0.25 * lenth)],
                       g_dist[int(0.5 * lenth)], g_dist[int(0.75 * lenth)], g_dist[int(0.9 * lenth)],
                       g_dist[int(0.9997 * lenth)], int(lenth - int(0.9997 * lenth)), float(int(info[0]) * 1.0 / total)]
            output.writerow(listdes)
        except:
            pass

if __name__ == '__main__':
    dataname=args.data_name
    data = load_data(dataname)

    # print  data[data["issue_date"] >='2013-05-01 00:00:00']["issue_date"][:2000]
    # print  len(data[data["issue_date"]>='2013-05-01 00:00:00']["issue_date"])
    # print  len(data[data["label_profit"]==0])
    # print  len(data[data["label_profit"] > 0])
    print len(data)
    des(data)