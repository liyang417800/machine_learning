#$encoding=utf-8
import pandas as pd

import csv
from scipy.interpolate import lagrange#拉格朗日函数
from pandas import Series,DataFrame, np
from numpy import nan as NA
import matplotlib.pyplot as plt


# data = pd.DataFrame({'男':[1,2,3,4,5,6,7,8],
#                    '女':[np.nan,5,7,8,9,10,11,12],
#                    '蛋白质':[5,np.nan,7,np.nan,9,10,11,12]
#                    },
#                     columns=['男','女','蛋白质'])
#
# print data

# feature_save_path = "./data/d_train_20180102.csv"  #将最终生成的特征存入该文件
feature_save_path = "./data/lable_pre.csv"  #将最终生成的特征存入该文件
data = pd.read_csv(feature_save_path)

# print data.describe().astype(np.int64).T
# print data['*天门冬氨酸氨基转换酶']
# data['*天门冬氨酸氨基转换酶'].plot()
# plt.show()

# print data['*天门冬氨酸氨基转换酶'].describe()

fig, ax = plt.subplots()
ax.scatter(x = data['*天门冬氨酸氨基转换酶'], y = data['血糖'])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)
plt.show()



#自定义列向量插值函数
# def ploy(s,n,k=3):
#     y=s[list(range(n-k,n))+list(range(n+1,n+1+k))]#取数
#     y=y[y.notnull()]
#     return lagrange(y.index,list(y))(n)
# for i in data.columns:
#     for j in range(len(data)):
#         if(data[i].isnull())[j]:
#             data[i][j]=ploy(data[i],j)
# data.to_csv('./data/lable_pre.csv',index=False)



# with open('./data/lable_pre.csv', "wb") as csvFile:
#     csvWriter = csv.writer(csvFile)
#     for i in range(len(data)):
#         print data[i]
#         csvWriter.writerow([data[i]])
#     csvFile.close



# data.to_excel('./data/1.xls')



# data=DataFrame(np.random.randn(1000,4))
# print(data.describe())
#
# print("\n....找出某一列中绝对值大小超过3的项...\n")
# col=data[3]
# print(col[np.abs(col) > 3] )
#
# print("\n....找出全部绝对值超过3的值的行...\n")
# print(col[(np.abs(data) > 3).any(1)] )











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

