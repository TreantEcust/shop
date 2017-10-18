import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# 对结果进行评估
def evaluate(pred):
    pred=pred[['row_id','real_shop_id','shop_id','pred']]
    pred.sort_values('pred', inplace=True)
    pred = pred.groupby('row_id').tail(1)
    return pred

train_feat=pd.read_csv('data/train_feat2.csv')
validation_feat=pd.read_csv('data/validation_feat2.csv')
predictors1 = ['wifi_jaccard', 'minutes', 'hot_point', 'wifi_union_count', 'dis_shop',
               'wifi_inter_count','mapk5','mapk10']
params = {
    'n_estimators':[30],
    'min_samples_leaf':[10],
    'class_weight':['balanced'],
    'max_features':[0.5],
    'max_depth':[5]
}
params=list(ParameterGrid(params))
train_data=np.array(train_feat[predictors1])
train_label=train_feat['label'].values
validation_data=np.array(validation_feat[predictors1])
for param in params:
    print(param)
    clf=RandomForestClassifier(n_estimators=param['n_estimators'], min_samples_leaf=param['min_samples_leaf'],
                               class_weight=param['class_weight'],max_features=param['max_features'],
                               max_depth=param['max_depth'],criterion='gini', random_state=0)
    clf.fit(train_data,train_label)
    pred=clf.predict_proba(validation_data)[:,1]
    validation_feat.loc[:, 'pred'] = pred
    result = evaluate(validation_feat)
    result.loc[:, 'result'] = (result['real_shop_id'] == result['shop_id']).astype('int')
    result = result['result'].values
    print('acc:' + str(sum(result) / len(result)))
    # feature importance
    feature_importance = list(clf.feature_importances_)
    y_pos = np.arange(len(predictors1))
    plt.barh(y_pos, feature_importance, align='center', alpha=0.2, color='b')
    plt.yticks(y_pos, predictors1)
    plt.show()