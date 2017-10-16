import numpy as np
import pandas as pd

# 计算两点之间距离
def cal_distance(lat1,lon1,lat2,lon2):
    dx = np.abs(lon1 - lon2)  # 经度差
    dy = np.abs(lat1 - lat2)  # 维度差
    b = (lat1 + lat2) / 2.0
    Lx = 6371004.0 * (dx / 57.2958) * np.cos(b / 57.2958)
    Ly = 6371004.0 * (dy / 57.2958)
    L = (Lx**2 + Ly**2) ** 0.5
    return L

# 购买和历史距离
def get_dis(result):
    result.loc[:, 'dis'] = cal_distance(result['latitude'].values, result['longitude'].values,
                                        result['latitude_train'].values, result['longitude_train'].values)
    return result

# 购买和店距离
def get_dis_shop(result):
    result.loc[:,'dis_shop']=cal_distance(result['latitude'].values, result['longitude'].values,
                                        result['latitude_shop'].values, result['longitude_shop'].values)
    return result

# 购买和历史时间差
def get_time_diff(result):
    result.loc[:,'time_diff']=abs(result['minutes']-result['minutes_train'])
    return result

# 购买和历史是否同属周末（或工作日)
def get_weekday_diff(result):
    result.loc[:,'weekday_diff']=abs(result['wday']-result['wday_train'])
    return result

# 添加店内热度
def get_hot_shop(train,result):
    #统计热度
    shop_hot_point=train.groupby('shop_id',as_index=False)['user_id'].agg({'hot_point':'count'})
    result=pd.merge(result,shop_hot_point,on='shop_id',how='left')
    result['hot_point'].fillna(0, inplace=True)
    return result

# 添加用户访问该店次数
def get_shop_times(train,result):
    user_shop_times=train.groupby(['user_id','shop_id'],as_index=False)['user_id'].agg({'user_shop_times':'count'})
    result=pd.merge(result,user_shop_times,on=['user_id','shop_id'],how='left')
    result['user_shop_times'].fillna(0, inplace=True)
    return result

def get_mall_times(train,result):
    user_mall_times = train.groupby(['user_id', 'mall_id'], as_index=False)['user_id'].agg({'user_mall_times': 'count'})
    result = pd.merge(result, user_mall_times, on=['user_id', 'mall_id'], how='left')
    result['user_mall_times'].fillna(0, inplace=True)
    return result

def get_shopmall(result):
    result.loc[:,'user_shopmall']=result['user_shop_times']/(result['user_mall_times']+0.0001)
    return result

def get_time(result):
    result.rename(columns={'time_stamp': 'time_min'}, inplace=True)
    return result

def get_wday(result):
    result.rename(columns={'wday':'is_wday'},inplace=True)
    return result

def get_wifi_count(result):
    result.rename(columns={'wifi_select':'wifi_count'},inplace=True)
    return result

def feat(train,result):
    ori_feat=list(result.columns)
    print('开始构造特征...')
    result = get_dis_shop(result)  # 购买和店距离
    result = get_hot_shop(train,result) # 添加店内热度
    result = get_shop_times(train,result) # 添加用户访问该店次数
    result = get_mall_times(train,result) #添加用户访问商场次数
    result = get_shopmall(result) #访问店次数/访问商场次数
    result = get_time(result) #时间作为特征rename
    result = get_wday(result) #是否周末为特征rename
    result = get_wifi_count(result) #wifi匹配数rename

    #特征统计
    final_feat=list(result.columns)
    final_feat=list(set(final_feat).difference(set(ori_feat)))
    print('特征构造完毕，特征一共'+str(len(final_feat))+'个，分别为：'+str(final_feat))
    return result