#$encoding=utf-8
'''
环境 ubuntu+IDEA+python35
实现的功能：利用GBDT模型实现数值的预测
背景：天池的IJICAI，预测商店流量
PS：feature_data.csv是已经处理好的特征
'''
import numpy as np
import pandas as pd
from sklearn import ensemble, cross_validation

#该评价指标用来评价模型好坏
def rmspe(zip_list,count):
    # w = ToWeight(y)
    # rmspe = np.sqrt(np.mean((y - yhat) ** 2))
    sum_value=0.0
    # count=len(zip_list)
    for real,predict in zip_list:
        v1=(real-predict)**2
        sum_value += v1
    v2=sum_value / count
    v3=np.sqrt(v2)
    return v3

#提取特征和目标值
def get_features_target(data):
    data_array=pd.np.array(data)#传入dataframe，为了遍历，先转为array
    features_list=[]
    target_list=[]
    for line in data_array:
        temp_list=[]
        for i in range(0,384):#一共有384个特征
            if i == 360 :#index=360对应的特征是flow
                target_temp=int(line[i])
            else:
                temp_list.append(int(line[i]))
        features_list.append(temp_list)
        target_list.append(target_temp)
    return features_list, target_list
    # return pd.DataFrame(features_list),pd.DataFrame(target_list)

def run_demo():

    feature_save_path = "/home/wangtuntun/IJCAI/Data/feature_data.csv"  # 将最终生成的特征存入该文件
    data = pd.read_csv(feature_save_path)
    data_other,data=cross_validation.train_test_split(data,test_size=0.001,random_state=10)#为了减少代码运行时间，方便测试
    train_and_valid, test = cross_validation.train_test_split(data, test_size=0.2, random_state=10)
    train, valid = cross_validation.train_test_split(train_and_valid, test_size=0.01, random_state=10)
    train_feature, train_target = get_features_target(train)
    test_feature, test_target = get_features_target(test)
    valid_feature, valid_target = get_features_target(valid)

    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
              'learning_rate': 0.01, 'loss': 'ls'}
    clf = ensemble.GradientBoostingRegressor(**params)

    clf.fit(train_feature, train_target) #训练
    # mse = mean_squared_error(test_target, clf.predict(test_feature)) #预测并且计算MSE
    # print(mse)
    pre=clf.predict(test_feature)
    pre_list=list(pre)
    real_pre_zip=zip(test_target,pre_list)

    count=len(pre_list)
    error=rmspe(real_pre_zip,count)
    print(error)

run_demo()

