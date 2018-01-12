#$encoding=utf-8
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
import pandas as pd
import csv

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


def get_features(data):
    data_array=pd.np.array(data)#传入dataframe，为了遍历，先转为array
    features_list=[]
    for line in data_array:
        temp_list=[]
        for i in range(0,41):
            if i == 1:
                if line[i]=="男":
                    line[i]=1
                else:
                    line[i]=0
            if i ==3:
                line[3] = line[3].replace('/','')
            temp_list.append(line[i])
        features_list.append(temp_list)
    return features_list

# 导入数据
# feature_save_path = "train_true.csv"  #将最终生成的特征存入该文件
feature_save_path = "d_train_20180102.csv"  #将最终生成的特征存入该文件
data = pd.read_csv(feature_save_path)
data = data.fillna(0)

# data.sort(["id"]) 排序
# data = data[0:100]
# print data


feature,lable = get_features_target(data)





feature_save_path_test = "d_test_A_20180102.csv"  #将最终生成的特征存入该文件
data_test = pd.read_csv(feature_save_path_test)
# print data_test.mean()
data_test = data_test.fillna(0)
# data.sort(["id"]) 排序
# data = data[0:100]
# print data
feature_test = get_features(data_test)


# print (feature_test[0:10])

X_train, X_test, y_train, y_test = train_test_split(feature, lable, test_size=0.01)

# print len(X_train), len(X_test), len(y_train), len(y_test)

# print(X_train)

# print(sorted(X_train,key=lambda x: (x[0], -x[1])))
# print y_train



"""初始化算法，设置参数

一些主要参数
loss: 损失函数，GBDT回归器可选'ls', 'lad', 'huber', 'quantile'。
learning_rate: 学习率/步长。
n_estimators: 迭代次数，和learning_rate存在trade-off关系。
criterion: 衡量分裂质量的公式，一般默认即可。
subsample: 样本采样比例。
max_features: 最大特征数或比例。

决策树相关参数包括max_depth, min_samples_split, min_samples_leaf, min_weight_fraction_leaf, max_leaf_nodes, min_impurity_split, 多数用来设定决策树分裂停止条件。

verbose: 日志level。
具体说明和其它参数请参考官网API。
"""
reg_model = GradientBoostingRegressor(
    loss='ls',
    learning_rate=0.02,
    n_estimators=220,
    subsample=0.75,
    max_features=0.1,
    max_depth=5,
    verbose=2
)

# 训练模型i
reg_model.fit(X_train, y_train)

# 评估模型
prediction_train = reg_model.predict(X_train)

# for i in range(len(X_train)):
#     print X_train[i][0],y_train[i],prediction_train[i]


rmse_train = mean_squared_error(y_train, prediction_train)
# prediction_test = reg_model.predict(feature_test)
prediction_test = reg_model.predict(X_test)

rmse_test = mean_squared_error(y_test, prediction_test)
# print prediction_test
# print round(prediction_test[0:2],3)

# with open('lable.csv', "wb") as csvFile:
#     csvWriter = csv.writer(csvFile)
#     for i in range(len(prediction_test)):
#         csvWriter.writerow([round(prediction_test[i],3)])
#     csvFile.close



print "RMSE for training dataset is %f, for testing dataset is %f." % (rmse_train, rmse_test)
"""Output:
RMSE for training dataset is 4.239157, for testing dataset is 10.749044.
"""
