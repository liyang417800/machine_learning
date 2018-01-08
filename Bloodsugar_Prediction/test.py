#$encoding=utf-8
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split

# 导入数据
X_train, X_test, y_train, y_test = train_test_split(load_boston().data, load_boston().target, test_size=0.2)


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
    n_estimators=200,
    subsample=0.8,
    max_features=0.8,
    max_depth=3,
    verbose=2
)

# 训练模型
reg_model.fit(X_train, y_train)

# 评估模型
prediction_train = reg_model.predict(X_train)
rmse_train = mean_squared_error(y_train, prediction_train)
prediction_test = reg_model.predict(X_test)
rmse_test = mean_squared_error(y_test, prediction_test)
print y_test,prediction_test
print "RMSE for training dataset is %f, for testing dataset is %f." % (rmse_train, rmse_test)
"""Output:
RMSE for training dataset is 4.239157, for testing dataset is 10.749044.
"""
