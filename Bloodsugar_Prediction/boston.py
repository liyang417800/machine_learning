#$encoding=utf-8
from sklearn.datasets import load_boston
from sklearn.cross_validation import train_test_split
import numpy as np


boston = load_boston()
# print(boston.data)

#数据分割

X=boston.data
y=boston.target
#随机擦痒25%的数据构建测试样本，剩余作为训练样本
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=33,test_size=0.25)

#分析回归目标值的差异
print("The max target value is",np.max(boston.target))
print("The min target value is",np.min(boston.target))
print("The average target value is",np.mean(boston.target))

#2.数据标准化处理
from sklearn.preprocessing import StandardScaler
#分别初始化对特征和目标值的标准化器
ss_X=StandardScaler()
ss_y=StandardScaler()

#分别对训练和测试数据的特征以及目标值进行标准化处理
X_train=ss_X.fit_transform(X_train)
X_test=ss_X.transform(X_test)
y_train=ss_y.fit_transform(y_train.reshape(-1,1))
y_test=ss_y.transform(y_test.reshape(-1,1))
