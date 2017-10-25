import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import ParameterGrid
import numpy as np
import matplotlib.pyplot as plt

train_feat=pd.read_csv('train_feat.csv')
train_label=train_feat.pop('label').values

validation_feat=pd.read_csv('validation_feat.csv')
validation_label=validation_feat.pop('label').values
feat_names=list(train_feat.columns)
categorical_feat_names=['wday']

label_mapping= pd.read_csv('multi_data/m_4341' + '/label_mapping.csv')
labels=label_mapping['label'].values
shops=label_mapping['shop_id'].values

params = {
    'num_class':[max(labels)+1],
    'metric': ['multi_error'],
    'objective': ['multiclass'],
    'learning_rate':[0.15],
    'feature_fraction': [0.8],
    'max_depth': [13],
    'num_leaves':[200],
    'bagging_fraction': [0.8],
    'bagging_freq':[5],
    'min_data_in_leaf':[15],
    'min_gain_to_split':[0],
    'num_iterations':[500],
    'lambda_l1':[0.01],
    'lambda_l2':[1],
    'verbose':[0],
    'is_unbalance':[True]
}
params=list(ParameterGrid(params))
lgbtrain=lgb.Dataset(train_feat,label=train_label,feature_name=feat_names,categorical_feature=categorical_feat_names)
lgbeval=lgb.Dataset(validation_feat,label=validation_label,reference=lgbtrain,feature_name=feat_names,
                    categorical_feature=categorical_feat_names)
lgbtest = validation_feat
for param in params:
    print(param)
    clf = lgb.train(param, lgbtrain, valid_sets=lgbeval, num_boost_round=param['num_iterations'],
                    early_stopping_rounds=50,
                    categorical_feature=categorical_feat_names)
    print('best interation:'+str(clf.best_iteration))
    pred = clf.predict(lgbtest)
    predict_label=np.argmax(pred,axis=1)
    result=validation_label-predict_label
    print('acc:'+str(len(np.nonzero(result==0)[0])/result.shape[0]))

    # # feature importance
    # feature_importance=list(clf.feature_importance())
    # y_pos = np.arange(len(feat_names))
    # plt.barh(y_pos,feature_importance,align = 'center',alpha = 0.2,color='b')
    # plt.yticks(y_pos,feat_names)
    # plt.show()