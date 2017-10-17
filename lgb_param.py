import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import ParameterGrid

pd.options.mode.chained_assignment = None
# 对结果进行评估
def evaluate(pred):
    pred=pred[['row_id','real_shop_id','shop_id','pred']]
    pred.sort_values('pred', inplace=True)
    pred = pred.groupby('row_id').tail(1)
    return pred

train_feat=pd.read_csv('data/train_feat3.csv')
validation_feat=pd.read_csv('data/validation_feat3.csv')
predictors1 = ['wifi_count','user_shop_times','dis_shop','hot_point']
predictors2 = ['wifi_count','dis_shop','hot_point']
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
lgbtrain1=lgb.Dataset(train_feat[predictors1],label=train_feat['label'],feature_name=predictors1)
lgbtrain2=lgb.Dataset(train_feat[predictors2],label=train_feat['label'],feature_name=predictors2)
lgbtest1 = validation_feat[predictors1]
lgbtest2 = validation_feat[predictors2]
for param in params:
    print(param)
    # model_cv=lgb.cv(param, lgbtrain, num_boost_round=200, nfold=5, metrics='binary_error',verbose_eval=True)
    # clf = lgb.train(param, lgbtrain1, num_boost_round=param['num_iterations'])
    # pred1 = clf.predict(lgbtest1)
    clf = lgb.train(param, lgbtrain2, num_boost_round=param['num_iterations'])
    pred2 = clf.predict(lgbtest2)
    validation_feat.loc[:,'pred'] = pred2
    result = evaluate(validation_feat)
    result.loc[:,'result']=(result['real_shop_id']==result['shop_id']).astype('int')
    result=result['result'].values
    print('acc:'+str(sum(result)/len(result)))
