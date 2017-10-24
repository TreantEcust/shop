import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import ParameterGrid
import numpy as np
import matplotlib.pyplot as plt

shop_path='../data/shop_info.csv'
shop_info = pd.read_csv(shop_path)
mall_list=list(set(shop_info['mall_id'].values))
total_num = 0
total_true = 0
for i,m in enumerate(mall_list):
    save_path='multi_data/'+m
    train_feat=pd.read_csv(save_path+'/train_feat.csv')
    train_label=train_feat['label'].values
    train_feat.drop('label',inplace=True,axis=1)

    validation_feat=pd.read_csv(save_path+'/validation_feat.csv')
    validation_label=validation_feat['label'].values
    validation_feat.drop('label',inplace=True,axis=1)
    feat_names=list(train_feat.columns)

    print('mall_id:'+m+' ('+str(i+1)+'/'+str(len(mall_list))+')')

    params = {
        'num_class':[max(train_label)+1],
        'objective': ['multiclass'],
        'learning_rate':[0.15],
        'feature_fraction': [0.8],
        'max_depth': [13],
        'num_leaves':[200],
        'bagging_fraction': [0.8],
        'bagging_freq':[5],
        'min_data_in_leaf':[15],
        'min_gain_to_split':[0],
        'num_iterations':[150],
        'lambda_l1':[0.01],
        'lambda_l2':[1],
        'verbose':[0],
        'is_unbalance':[True]
    }
    params=list(ParameterGrid(params))
    lgbtrain=lgb.Dataset(train_feat,label=train_label,feature_name=feat_names)
    lgbtest = validation_feat
    for param in params:
        clf = lgb.train(param, lgbtrain, num_boost_round=param['num_iterations'])
        pred = clf.predict(lgbtest)
        predict_label=np.argmax(pred,axis=1)
        result=validation_label-predict_label
        print('acc:'+str(len(np.nonzero(result==0)[0])/result.shape[0]))
        total_num+=result.shape[0]
        total_true+=len(np.nonzero(result==0)[0])
    print('total acc:'+str(total_true/total_num))

below80_list=['m_6337','m_5529','m_2224','m_4187','m_4079','m_1293','m_4094','m_1377'
    ,'m_7168','m_2058','m_4011','m_7973','m_2878','m_5825','m_3054','m_3501','m_6803'
    ,'m_1920','m_3839','m_1263','m_7601','m_6167','m_7800']