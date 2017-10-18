import pandas as pd
from tqdm import tqdm
from scipy.spatial.distance import jaccard

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

#获取wifi数匹配度最高的N个店作为负样本
def get_wifi(test,shop_info):
    N=10
    wifi_test=test[['row_id','wifi_dis']].values
    wifi_shop=shop_info[['shop_id','wifi_avgdis_shop']].values
    wifi_shop_dict={}
    wifi_test_dict={}
    for i in tqdm(range(wifi_test.shape[0])):
        wifi_test_dict[wifi_test[i,0]]=set(eval(wifi_test[i,1]))
    for i in tqdm(range(wifi_shop.shape[0])):
        wifi_shop_dict[wifi_shop[i,0]]=set(eval(wifi_shop[i,1]))
    result=pd.merge(test,shop_info,on='mall_id',how='left')
    result.drop(['wifi_dis', 'wifi_avgdis_shop','wifi_counts_shop'], axis=1, inplace=True)
    # result=result.loc[0:43946,:]
    wifi_inter_count=[]
    wifi_union_count=[]
    for i in tqdm(range(result.shape[0])):
        wifi_inter_count.append \
            (len(wifi_shop_dict[result.loc[i, 'shop_id']] & wifi_test_dict[result.loc[i, 'row_id']]))
        wifi_union_count.append \
            (len(wifi_shop_dict[result.loc[i, 'shop_id']] | wifi_test_dict[result.loc[i, 'row_id']]))
    result.loc[:, 'wifi_inter_count'] = wifi_inter_count
    result.loc[:, 'wifi_union_count'] = wifi_union_count
    result = result[(result['wifi_inter_count'] >= 1)]
    result.loc[:, 'wifi_jaccard'] = result['wifi_inter_count']/(result['wifi_union_count'])
    result.sort_values('wifi_inter_count',inplace=True)
    result = result.groupby('row_id').tail(N)

    return result

def make(test, shop_info,type=None):
    print('构造负类样本...')
    pd.options.mode.chained_assignment = None  # default='warn'
    # user_history_shop=get_user_history(train,test,shop_info)
    # nearest_shop=get_nearest(train,test,shop_info)
    result=get_wifi(test,shop_info)
    result.sort_values('row_id', inplace=True)
    # result= pd.concat([user_history_shop,nearest_shop])#不去重
    print('负类样本构造完毕，总数：'+str(result.shape[0]))

    if type!='test':
        #临时统计正确结果的覆盖率
        result.loc[:,'label_temp']=(result['real_shop_id']==result['shop_id']).astype('int')
        result_temp=result[(result['label_temp']==1)][['row_id','label_temp']].drop_duplicates()
        total_num=result['row_id'].drop_duplicates()
        print('正类样本覆盖率：'+str(result_temp.shape[0]/total_num.shape[0]))
        result.drop('label_temp', axis=1, inplace=True)

    return result
