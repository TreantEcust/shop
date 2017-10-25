import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import ParameterGrid
import numpy as np

shop_path='../data/shop_info.csv'
shop_info = pd.read_csv(shop_path)
mall_list=list(set(shop_info['mall_id'].values))
total_num = 0
total_true = 0
save_mall_list=[]
save_acc_list=[]
for i,m in enumerate(mall_list):
    save_path='multi_data/'+m
    train_feat=pd.read_csv(save_path+'/train_feat.csv')
    train_label=train_feat.pop('label').values

    validation_feat=pd.read_csv(save_path+'/validation_feat.csv')
    validation_label=validation_feat.pop('label').values
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
    save_mall_list.append(m)
    save_acc_list.append(len(np.nonzero(result==0)[0])/result.shape[0])
result_mall=pd.DataFrame([save_mall_list,save_acc_list],index=['mall_id','accuracy'])
result_mall=result_mall.transpose()
result_mall.to_csv('result_mall.csv')