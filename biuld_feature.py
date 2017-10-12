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
    result.loc[:,'time_diff']=0
    return result

# 购买和历史是否同属周末（或工作日)
def get_weekday_diff(result):
    result.loc[:,'weekday_diff']=0
    return result

# 添加店内热度
def get_hot_shop(train,result,shop_info):
    result.loc[:,'hot_point']=0
    return result

#
def get_user_times(result):
    result.loc[:,'user_times']=0
    return result

def feat(train,result,shop_info):
    ori_feat=list(result.columns)
    print('开始构造特征...')
    result = get_dis(result)  # 购买和历史距离
    result = get_dis_shop(result)  # 购买和店距离
    result = get_time_diff(result)  # 购买和历史时间差
    result = get_weekday_diff(result)  # 购买和历史是否同属周末（或工作日）
    result = get_hot_shop(train,result,shop_info) # 添加店内热度
    result = get_user_times(result) # 添加用户访问该店次数

    #特征统计
    final_feat=list(result.columns)
    final_feat=list(set(final_feat).difference(set(ori_feat)))
    print('特征构造完毕，特征一共'+str(len(final_feat))+'个，分别为：'+str(final_feat))
    return result