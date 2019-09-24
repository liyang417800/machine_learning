# coding:utf-8

import numpy as np
import pandas as pd
import matplotlib.dates as mdates    #處理日期
import matplotlib.pyplot as plt

#讀入日期
df = pd.read_csv('/Users/yangli/PycharmProjects/machine_learning/Http_Plot/Data/results.csv')
x = df['time']
x = pd.to_datetime(x)               #轉換為日期，否則下面的日期設置不會生效
print x

y = df['drop']
# print y
#plt.gca()函數獲得當前坐標軸，然後才能設置參數或作圖，plt.plot()內部實現了這一步驟
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  #設置x軸主刻度顯示格式（日期）
plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%M'))  #設置x軸主刻度間距

plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.title("Daily Precipitation Statistics",fontsize=24)
plt.xlabel('Time Minute',fontsize=16)

plt.ylabel("Drop Rain",fontsize=16)
# plt.tick_params(axis='both',which='major',labelsize=10)
for a, b in zip(x, y):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.plot(x,y,c='red')
plt.savefig('/Users/yangli/PycharmProjects/machine_learning/Http_Plot/Data/DropRain.jpg')
plt.show()




