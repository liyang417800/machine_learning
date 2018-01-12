#$encoding=utf-8
import pandas as pd
import numpy as np
import csv

# df = pd.DataFrame({'男':[1,2,3,4,5,6,7,8],
#                    '女':[np.nan,5,7,8,9,10,11,12],
#                    '蛋白质':[5,np.nan,7,np.nan,9,10,11,12]
#                    },
#                     columns=['男','女','蛋白质'],
#                     index=list('ABCDEFGH'))

feature_save_path = "d_train_20180102.csv"  #将最终生成的特征存入该文件
df = pd.read_csv(feature_save_path)
column = df.columns.values

# 只留下需要处理的列


# print(df)
column = df.columns.values
print column
# print df['白球比例'].mean()

for i in range(len(column)):
    print i
    if i>=4:
        a = df[column[i]].mean()
        df = df.fillna({column[i]:a})
    i=i+1
print len(df)
print type(df)
# del df[0]
df.to_csv('train_true.csv',index=False)

# for i in range(len(df)):
#     print i



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

