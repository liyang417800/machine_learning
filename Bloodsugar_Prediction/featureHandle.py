#$encoding=utf-8
#https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard
import pandas as pd

import csv
from scipy.interpolate import lagrange#拉格朗日函数
from pandas import Series,DataFrame, np
from numpy import nan as NA
import matplotlib.pyplot as plt

import seaborn as sns

# from Bloodsugar_Prediction import bloodsugar

color = sns.color_palette()
sns.set_style('darkgrid')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt  # Matlab-style plotting
color = sns.color_palette()
sns.set_style('darkgrid')
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning (from sklearn and seaborn)


from scipy import stats
from scipy.stats import norm, skew #for some statistics


pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x)) #Limiting floats output to 3 decimal points


from subprocess import check_output

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# data = pd.DataFrame({'男':[1,2,3,4,5,6,7,8],
#                    '女':[np.nan,5,7,8,9,10,11,12],
#                    '蛋白质':[5,np.nan,7,np.nan,9,10,11,12]
#                    },
#                     columns=['男','女','蛋白质'])
#
# print data

feature_save_path = "./data/d_train_20180102.csv"  #将最终生成的特征存入该文件
# feature_save_path = "./data/lable_pre.csv"  #将最终生成的特征存入该文件
data = pd.read_csv(feature_save_path)
# data.fillna(data.median(axis=0),inplace=True)

feature_save_path_t = "./data/d_test_A_20180102.csv"  #将最终生成的特征存入该文件
# feature_save_path = "./data/lable_pre.csv"  #将最终生成的特征存入该文件
test = pd.read_csv(feature_save_path_t)
# test.fillna(data.median(axis=0),inplace=True)


#特征重要性
# from sklearn.cross_validation import cross_val_score, ShuffleSplit
# # from sklearn.datasets import load_boston
# from sklearn.ensemble import RandomForestRegressor
#
# def get_features_target(data):
#     data_array=pd.np.array(data)#传入dataframe，为了遍历，先转为array
#     features_list=[]
#     target_list=[]
#     for line in data_array:
#         temp_list=[]
#         for i in range(0,42):
#             if i == 1:
#                 if line[i]=="男":
#                     line[i]=1
#                 else:
#                     line[i]=0
#             if i ==3:
#                 line[3] = line[3].replace('/','')
#             if i == 41 :
#                 target_temp=(line[i])
#             else:
#                 temp_list.append(line[i])
#         features_list.append(temp_list)
#         target_list.append(target_temp)
#     return features_list, target_list
# feature_save_path = "./data/d_train_20180102.csv"  #将最终生成的特征存入该文件
# # feature_save_path = "./data/lable_pre.csv"  #将最终生成的特征存入该文件
# data = pd.read_csv(feature_save_path)
#
# data = data.fillna(0)
#
# feature,lable = get_features_target(data)
# names = list(data.columns)
# # print names
# feature = np.array(feature)
# # print feature.head()
# # print feature[:, 0:0+1]
#
# rf = RandomForestRegressor(n_estimators=20, max_depth=4)
# scores = []
#
# for i in range(feature.shape[1]):
#      score = cross_val_score(rf, feature[:, i:i+1], lable, scoring="r2",
#                               cv=ShuffleSplit(len(feature), 3, .3))
#      scores.append((round(np.mean(score), 3), names[i]))
# print sorted(scores, reverse=True)



# print data['*天门冬氨酸氨基转换酶']

# print data.describe().astype(np.int64).T
# print data['*天门冬氨酸氨基转换酶']
# data['*天门冬氨酸氨基转换酶'].plot()
# plt.show()

# print data['*天门冬氨酸氨基转换酶'].describe()

# 画图删除数据（离群值）
# 训练数据中可能存在其他离群值。然而，如果测试数据中也有异常值，除去所有这些可能会严重影响我们的模型。这就是为什么我们不把它们全部移除，而是设法使我们的一些模型对它们健壮。你可以参考这个笔记本的造型部分。
# fig, ax = plt.subplots()
# ax.scatter(x = data['*天门冬氨酸氨基转换酶'], y = data['血糖'])
# plt.ylabel('血糖', fontsize=13)
# plt.xlabel('天门冬氨酸氨基转换酶', fontsize=13)
# plt.show()

#
#
# train = data.drop(data[(data['血糖']>20)].index)
# fig, ax = plt.subplots()
# ax.scatter(x = train['*天门冬氨酸氨基转换酶'], y = train['血糖'])
# plt.ylabel('血糖', fontsize=13)
# plt.xlabel('天门冬氨酸氨基转换酶', fontsize=13)
# plt.show()

#Target Variable（目标变量分析）
# mu = 5.63 and sigma = 1.54
# sns.distplot(data['血糖'] , fit=norm);
#
# # # Get the fitted parameters used by the function
# (mu, sigma) = norm.fit(data['血糖'])
# print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
# #
# # #Now plot the distribution
# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
#             loc='best')
# plt.ylabel('Frequency')
# plt.title('血糖 distribution')
# #
# # #Get also the QQ-plot
# fig = plt.figure()
# res = stats.probplot(data['血糖'], plot=plt)
# plt.show()


# data["血糖"] = np.log1p(data["血糖"])
#
# #Check the new distribution
# sns.distplot(data['血糖'] , fit=norm);
#
# # Get the fitted parameters used by the function
# (mu, sigma) = norm.fit(data['血糖'])
# print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
#
# #Now plot the distribution
# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
#             loc='best')
# plt.ylabel('Frequency')
# plt.title('血糖 distribution')
#
# #Get also the QQ-plot
# fig = plt.figure()
# res = stats.probplot(data['血糖'], plot=plt)
# plt.show()

#Features engineering 特征工程
#1 Missing Data 缺失值的统计判断
# ntrain = data.shape[0]
# ntest = test.shape[0]
# y_train = data['血糖'].values
# all_data = pd.concat((data, test)).reset_index(drop=True)
# all_data.drop(['血糖'], axis=1, inplace=True)
# print("all_data size is : {}".format(all_data.shape)) #all_data size is : (6642, 41)
# #
# all_data_na = (all_data.isnull().sum() / len(all_data)) * 100
# all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)[:30]
# missing_data = pd.DataFrame({'Missing Ratio' :all_data_na})
# print missing_data.head(20)
# #
# f, ax = plt.subplots(figsize=(15, 12))
# plt.xticks(rotation='90')
# sns.barplot(x=all_data_na.index, y=all_data_na)
# plt.xlabel('Features', fontsize=15)
# plt.ylabel('Percent of missing values', fontsize=15)
# plt.title('Percent missing data by feature', fontsize=15)
# plt.show()

# Data Correlation 数据相关性判断
# Correlation map to see how features are correlated with SalePrice
# corrmat = data.corr()
# plt.subplots(figsize=(12,9))
# sns.heatmap(corrmat, vmax=0.9, square=True)
# plt.show()

#Imputing missing values
#0，均值，中位数等
#Adding one more important feature
# 需要查看官方文档，找到现有特征的联系，进行新特征的衍生
# all_data['TotalSF'] = all_data['TotalBsmtSF'] + all_data['1stFlrSF'] + all_data['2ndFlrSF']

# numeric_feats = data.dtypes[data.dtypes != "object"].index
# #
# # # Check the skew of all numerical features
# skewed_feats = data[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
# print("\nSkew in numerical features: \n")
# skewness = pd.DataFrame({'Skew' :skewed_feats})
# print skewness.head(10)
# #
# skewness = skewness[abs(skewness) > 0.75]
# print("There are {} skewed numerical features to Box Cox transform".format(skewness.shape[0]))
# #
# from scipy.special import boxcox1p
# skewed_features = skewness.index
# lam = 0.15
# for feat in skewed_features:
#     #all_data[feat] += 1
#     data[feat] = boxcox1p(data[feat], lam)
#
#
# numeric_feats = data.dtypes[data.dtypes != "object"].index
#
# # Check the skew of all numerical features
# skewed_feats = data[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
# print("\nSkew in numerical features: \n")
# skewness = pd.DataFrame({'Skew' :skewed_feats})
# print skewness.head(10)

#Select Variables
# print data['血糖'].describe()
# sns.distplot(data['血糖']);
# plt.show()





















#---------------------------------------------------
# 只留下需要处理的列
# print(df)
# column = df.columns.values
#
# for i in range(len(column)):
#     print i
#     if i>=4:
#         a = df[column[i]].mean()
#         df = df.fillna({column[i]:a})
#     i=i+1
# print len(df)
# df.to_csv('train_true.csv',index=False)

# with open('train_true.csv', "wb") as csvFile:
#     csvWriter = csv.writer(csvFile)
#     csvWriter.writerow(df)
#     csvFile.close




# 依次处理每一列
# for col in cols:
#     na_series = df_na[col]
#     names = list(df.loc[na_series,gp_col])
#
#     t = df_mean.loc[names,col]
#     t.index = df.loc[na_series,col].index
#
#     # 相同的index进行赋值
#     df.loc[na_series,col] = t

