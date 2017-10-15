import pandas as pd
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from scipy.spatial.distance import cdist

#加入用户在train中去过的店铺作为负样本
def get_user_history(train,test,shop_info):
    train = pd.merge(train, shop_info, on=['shop_id'], how='left').drop('mall_id', axis=1)
    result = pd.merge(test,train,on='user_id',how='left')
    result.dropna(axis=0, how='any',inplace=True)

    return result

#获取目标点最近(经纬度简单曼哈顿距离)的N个店作为负样本
def get_nearest(train,test,shop_info):
    N=15#N近邻
    result=pd.merge(test,shop_info,on='mall_id',how='left')
    result.loc[:, 'shop_dis'] = abs(result['longitude'] - result['longitude_shop']) + abs(
        result['latitude'] - result['latitude_shop'])
    result.sort_values('shop_dis', inplace=True,ascending=False)
    result = result.groupby('row_id').tail(N)

    #补全用户历史信息
    result=pd.merge(result,train,on=['user_id','shop_id'],how='left')#无需去除na
    #删去shop_dis
    result.drop('shop_dis', axis=1, inplace=True)

    return result

def wifi_select(x):
    print(x['row_id'])
    x1=set(list(eval(x['wifi_infos_shop']).keys()))
    x2=set(list(map(lambda q:q.split('|')[0],x['wifi_infos'].split(';'))))
    x['wifi_select']=len(x1&x2)
    return x

#获取wifi数匹配度最高的N个店作为负样本
def get_wifi(test,shop_info):
    N=10
    wifi_avgdis_shop=np.array(list(map(lambda x:eval(x),shop_info['wifi_avgdis_shop'].values)))
    wifi_avgdis_test = np.array(list(map(lambda x: eval(x), test['wifi_dis'].values)))
    FH = FeatureHasher(n_features=1000)
    wifi_avgdis_shop=FH.transform(wifi_avgdis_shop).toarray()
    wifi_avgdis_test=FH.transform(wifi_avgdis_test).toarray()

    result=pd.merge(test,shop_info,on='mall_id',how='left')
    X_dis = cdist(wifi_avgdis_test, wifi_avgdis_shop)

    result.loc[:,'wifi_select']=0
    result=result.apply(lambda x:wifi_select(x),axis=1)
    result=result[(result['wifi_select']>=1)]
    result.sort_values('wifi_select',inplace=True)
    result = result.groupby('row_id').tail(N)

    # 补全用户历史信息
    # result = pd.merge(result, train, on=['user_id', 'shop_id'], how='left')  # 无需去除na
    # 删去wifi_select
    # result.drop('wifi_select', axis=1, inplace=True)

    return result

def make(train, test, shop_info):
    print('构造负类样本...')
    # user_history_shop=get_user_history(train,test,shop_info)
    # nearest_shop=get_nearest(train,test,shop_info)
    most_wifi_shop=get_wifi(test,shop_info)
    #负类样本汇总
    result=most_wifi_shop
    # result= pd.concat([user_history_shop,nearest_shop])#不去重
    print('负类样本构造完毕，总数：'+str(result.shape[0]))

    #临时统计正确结果的覆盖率
    result.loc[:,'label_temp']=(result['real_shop_id']==result['shop_id']).astype('int')
    result_temp=result[(result['label_temp']==1)][['row_id','label_temp']].drop_duplicates()
    total_num=result['row_id'].drop_duplicates()
    print('正类样本覆盖率：'+str(result_temp.shape[0]/total_num.shape[0]))
    result.drop('label_temp', axis=1, inplace=True)

    return result
