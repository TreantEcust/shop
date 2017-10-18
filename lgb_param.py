import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np
import matplotlib.pyplot as plt


pd.options.mode.chained_assignment = None
# 对结果进行评估
def evaluate(pred):
    pred=pred[['row_id','real_shop_id','shop_id','pred']]
    pred.sort_values('pred', inplace=True)
    pred = pred.groupby('row_id').tail(1)
    return pred

train_feat=pd.read_csv('data/train_feat.csv')
validation_feat=pd.read_csv('data/validation_feat.csv')
predictors1 = ['wday', 'wifi_jaccard', 'minutes', 'hot_point', 'wifi_union_count', 'dis_shop', 'wifi_inter_count']
params = {
    'objective': ['binary'],
    'learning_rate':[0.2],
    'feature_fraction': [1],
    'max_depth': [5],
    'num_leaves':[31],
    'bagging_fraction': [0.8],
    'bagging_freq':[5],
    'min_data_in_leaf':[10],
    'min_gain_to_split':[0],
    'num_iterations':[50],
    'lambda_l1':[1],
    'lambda_l2':[1],
    'verbose':[0],
    'is_unbalance':[True]
}
params=list(ParameterGrid(params))
lgbtrain1=lgb.Dataset(train_feat[predictors1],label=train_feat['label'],feature_name=predictors1)
lgbtest1 = validation_feat[predictors1]
for param in params:
    print(param)
    # model_cv=lgb.cv(param, lgbtrain, num_boost_round=200, nfold=5, metrics='binary_error',verbose_eval=True)
    clf = lgb.train(param, lgbtrain1, num_boost_round=param['num_iterations'])
    pred1 = clf.predict(lgbtest1)
    validation_feat.loc[:,'pred'] = pred1
    result = evaluate(validation_feat)
    result.loc[:,'result']=(result['real_shop_id']==result['shop_id']).astype('int')
    result=result['result'].values
    print('acc:'+str(sum(result)/len(result)))
    # feature importance
    feature_importance=list(clf.feature_importance())
    y_pos = np.arange(len(predictors1))
    plt.barh(y_pos,feature_importance,align = 'center',alpha = 0.2,color='b')
    plt.yticks(y_pos,predictors1)
    plt.show()
