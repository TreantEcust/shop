import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np

pd.options.mode.chained_assignment = None
# 对结果进行评估
def evaluate(pred):
    pred=pred[['row_id','shop_id','pred']]
    pred.sort_values('pred', inplace=True)
    pred = pred.groupby('row_id').tail(1)
    return pred

train_feat=pd.read_csv('data/train_feat3.csv')
validation_feat=pd.read_csv('data/validation_feat3.csv')
test_feat=pd.read_csv('data/test_feat3.csv')
predictors = ['wifi_count','dis_shop','hot_point']
params = {
    'objective': ['binary'],
    'learning_rate':[0.2],
    'feature_fraction': [0.9],
    'max_depth': [5],
    'num_leaves':[31],
    'bagging_fraction': [0.8],
    'bagging_freq':[5],
    'min_data_in_leaf':[30],
    'min_gain_to_split':[0],
    'num_iterations':[50],
    'lambda_l1':[1],
    'lambda_l2':[1],
    'verbose':[0],
    'is_unbalance':[True]
}
params=list(ParameterGrid(params))
train_data=pd.concat([train_feat[predictors],validation_feat[predictors]])
train_label=pd.concat([train_feat['label'],validation_feat['label']])
lgbtrain=lgb.Dataset(train_data,label=train_label,feature_name=predictors)
lgbtest = test_feat[predictors]
for param in params:
    print(param)
    clf = lgb.train(param, lgbtrain, num_boost_round=param['num_iterations'])
    test_feat.loc[:,'pred'] = clf.predict(lgbtest)
    result = evaluate(test_feat)
    result = result[['row_id','shop_id']]
real_test=pd.read_csv('data/test_data.csv')
real_test=real_test[['row_id']]
result=pd.merge(real_test,result,on='row_id',how='left')
result.to_csv('result.csv',index=False)
