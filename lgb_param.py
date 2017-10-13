import lightgbm as lgb
import pandas as pd
pd.options.mode.chained_assignment = None
# 对结果进行评估
def evaluate(pred):
    pred=pred[['row_id','real_shop_id','shop_id','pred']]
    pred.sort_values('pred', inplace=True)
    pred = pred.groupby('row_id').tail(1)
    return pred

train_feat=pd.read_csv('data/train_feat.csv')
validation_feat=pd.read_csv('data/validation_feat.csv')

predictors = ['dis','dis_shop','time_diff','weekday_diff','hot_point','user_times']
params = {
    'objective': 'binary',
    'learning_rate':0.2,
    'feature_fraction': 0.85,
    'max_depth': 6,
    'num_leaves':60,
    'bagging_fraction': 0.85,
    'bagging_freq':5,
    'min_data_in_leaf':50,
    'min_gain_to_split':0,
    'num_iterations':100,
    'lambda_l1':1,
    'lambda_l2':1,
    'verbose':0,
    'is_unbalance':True
}
print(params)
lgbtrain=lgb.Dataset(train_feat[predictors],label=train_feat['label'])
# model_cv=lgb.cv(params, lgbtrain, num_boost_round=300, nfold=5, metrics='binary_error',verbose_eval=True)
clf=lgb.train(params,lgbtrain,num_boost_round=100)
lgbtest = validation_feat[predictors]
validation_feat.loc[:,'pred'] = clf.predict(lgbtest)
result = evaluate(validation_feat)
result.loc[:,'result']=(result['real_shop_id']==result['shop_id']).astype('int')
result=result['result'].values
print('acc:'+str(sum(result)/len(result)))
