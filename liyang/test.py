#coding:utf-8
import pandas as pd

import csv
from scipy.interpolate import lagrange#拉格朗日函数
from pandas import Series,DataFrame, np
from numpy import nan as NA
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor


def get_features_target(data):
    data_array=pd.np.array(data)#传入dataframe，为了遍历，先转为array
    features_list=[]
    target_list=[]
    for line in data_array:
        temp_list=[]
        for i in range(0,42):
            if i == 1:
                if line[i]=="男":
                    line[i]=1
                else:
                    line[i]=0
            if i ==3:
                line[3] = line[3].replace('/','')
            if i == 41 :
                target_temp=(line[i])
            else:
                temp_list.append(line[i])
        features_list.append(temp_list)
        target_list.append(target_temp)
    return features_list, target_list
feature_save_path = "C:\Users\Administrator\machine_learning\Bloodsugar_Prediction\data\d_train_20180102.csv"  #将最终生成的特征存入该文件
# feature_save_path = "./data/lable_pre.csv"  #将最终生成的特征存入该文件
data = pd.read_csv(feature_save_path)

data = data.fillna(0)

feature,lable = get_features_target(data)
names = list(data.columns)
# print names
feature = np.array(feature)
# print feature.head()
print feature[:, 0:0+1]

rf = RandomForestRegressor(n_estimators=20, max_depth=4)
scores = []

for i in range(feature.shape[1]):
     score = cross_val_score(rf, feature[:, i:i+1], lable, scoring="r2",
                              cv=ShuffleSplit(len(feature), 3, .3))
     scores.append((round(np.mean(score), 3), names[i]))
print sorted(scores, reverse=True)










# from sklearn.cross_validation import cross_val_score, ShuffleSplit
# from sklearn.datasets import load_boston
# from sklearn.ensemble import RandomForestRegressor
#
# #Load boston housing dataset as an example
# boston = load_boston()
# X = boston["data"]
# Y = boston["target"]
# names = boston["feature_names"]
# print type(X)
#
# rf = RandomForestRegressor(n_estimators=20, max_depth=4)
# scores = []
# for i in range(X.shape[1]):
#      score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",
#                               cv=ShuffleSplit(len(X), 3, .3))
#      scores.append((round(np.mean(score), 3), names[i]))
# print sorted(scores, reverse=True)






