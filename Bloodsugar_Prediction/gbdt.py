#coding:utf-8
import time
import datetime
import numpy as np
import pandas as pd
import lightgbm as lgb
from dateutil.parser import parse
from scipy.stats import skew
from sklearn.cross_validation import KFold
from sklearn.metrics import mean_squared_error

import sys
reload(sys)
sys.setdefaultencoding('utf8')



data_path = './data/'

train = pd.read_csv(data_path+'d_train_20180102.csv')
test = pd.read_csv(data_path+'d_test_A_20180102.csv')

#0.975342143934
#删除特征重要性低的特征:尿酸,高密度脂蛋白胆固醇
# train = train.drop('乙肝表面抗原',1)
train = train.drop('乙肝e抗体',1)
# test = test.drop('乙肝表面抗原',1)
test = test.drop('乙肝e抗体',1)
# train["血糖"] = np.log1p(train["血糖"])
train = train.drop(train[(train['血糖']>25)].index)

all_data = pd.concat((train, test)).reset_index(drop=True)


numeric_feats = all_data.dtypes[all_data.dtypes != "object"].index

# Check the skew of all numerical features
skewed_feats = all_data[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
print("\nSkew in numerical features: \n")
skewness = pd.DataFrame({'Skew' :skewed_feats})
skewness.head(10)

skewness = skewness[abs(skewness) > 0.75]
print("There are {} skewed numerical features to Box Cox transform".format(skewness.shape[0]))

from scipy.special import boxcox1p
skewed_features = skewness.index
lam = 0.15
for feat in skewed_features:
    #all_data[feat] += 1
    all_data[feat] = boxcox1p(all_data[feat], lam)
all_data[skewed_features] = np.log1p(all_data[skewed_features])

# ntrain = train.shape[0]
# ntest = test.shape[0]
# train = all_data[:ntrain]
# test = all_data[ntrain:]





def make_feat(train,test):
    train_id = train.id.values.copy()
    test_id = test.id.values.copy()
    data = pd.concat([train,test])


    data['性别'] = data['性别'].map({'男':1,'女':0})
    data['体检日期'] = (pd.to_datetime(data['体检日期']) - parse('2017-10-09')).dt.days

    data.fillna(data.median(axis=0),inplace=True)
    # print data

    train_feat = data[data.id.isin(train_id)]
    test_feat = data[data.id.isin(test_id)]

    return train_feat,test_feat



train_feat,test_feat = make_feat(train,test)



predictors = [f for f in test_feat.columns if f not in ['血糖']]


def evalerror(pred, df):
    label = df.get_label().values.copy()
    score = mean_squared_error(label,pred)*0.5
    return ('0.5mse',score,False)

print('开始训练...')
params = {
    'learning_rate': 0.01,
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'mse',
    'sub_feature': 0.7,
    'num_leaves': 60,
    'colsample_bytree': 0.7,
    'feature_fraction': 0.7,
    'min_data': 100,
    'min_hessian': 1,
    'verbose': -1,
}

print('开始CV 5折训练...')
t0 = time.time()
train_preds = np.zeros(train_feat.shape[0]) #(5642, 42)
# print train_preds,train_feat.shape
test_preds = np.zeros((test_feat.shape[0], 5))
# print test_preds,test_feat.shape
kf = KFold(len(train_feat), n_folds = 5, shuffle=True, random_state=520)
for i, (train_index, test_index) in enumerate(kf):
    print('第{}次训练...'.format(i))
    print i, (train_index, test_index)
    train_feat1 = train_feat.iloc[train_index]
    train_feat2 = train_feat.iloc[test_index]
    lgb_train1 = lgb.Dataset(train_feat1[predictors], train_feat1['血糖'],categorical_feature=['性别'])
    lgb_train2 = lgb.Dataset(train_feat2[predictors], train_feat2['血糖'])
    gbm = lgb.train(params,
                    lgb_train1,
                    num_boost_round=3000,
                    valid_sets=lgb_train2,
                    verbose_eval=100,
                    feval=evalerror,
                    early_stopping_rounds=100)
    feat_imp = pd.Series(gbm.feature_importance(), index=predictors).sort_values(ascending=False)
    train_preds[test_index] += gbm.predict(train_feat2[predictors])
    test_preds[:,i] = gbm.predict(test_feat[predictors])
print('线下得分：    {}'.format(mean_squared_error(train_feat['血糖'],train_preds)*0.5))
print('CV训练用时{}秒'.format(time.time() - t0))

submission = pd.DataFrame({'pred':test_preds.mean(axis=1)})
submission.to_csv(r'sub{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')),header=None,
                  index=False, float_format='%.4f')