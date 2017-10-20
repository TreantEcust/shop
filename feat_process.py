import pandas as pd
import gc
from tqdm import tqdm

train_path='data/train_data.csv'
test_path='data/test_data.csv'
shop_path='data/shop_info.csv'

train_feat_path='data/train_feat2.csv'
test_feat_path='data/test_feat2.csv'
validation_feat_path='data/validation_feat2.csv'

train_feat_path2='data/train_feat2.csv'
test_feat_path2='data/test_feat2.csv'
validation_feat_path2='data/validation_feat2.csv'

def nor_process(result,predictors):
    #candidate
    cand_num=result.groupby('row_id', as_index=False)['row_id'].agg({'cand_num': 'count'})
    result=pd.merge(result, cand_num, on='row_id', how='left')

    for p in predictors:
        print(p)
        temp_max = result.groupby('row_id', as_index=False)[p].agg({'max' + p: 'max'})
        temp_min = result.groupby('row_id', as_index=False)[p].agg({'min' + p: 'min'})
        result = pd.merge(result, temp_max, on='row_id', how='left')
        result = pd.merge(result, temp_min, on='row_id', how='left')
        result[p]=(result[p]-result['min'+p])/(result['max'+p]-result['min'+p]+0.0001)
        result.drop(['max'+p,'min'+p],inplace=True,axis=1)

    return result

def apk(actual, predicted, k=10,on_actual=True):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if len(predicted)>k:
        predicted = predicted[:k]
    if len(actual)>k and on_actual:
        actual = actual[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)

def ssid_sub(actual, predicted):
    large_sum=0
    large_num=0
    less_sum=0
    less_num=0
    for k1 in actual:
        if k1 in predicted:
            if predicted[k1]>=actual[k1]:
                large_sum+=(predicted[k1]-actual[k1])
                large_num+=1
            else:
                less_sum+=(actual[k1]-predicted[k1])
                less_num+=1
    large_sum/=(large_num+0.0001)
    less_sum/=(less_num+0.0001)
    return large_sum,large_num,less_sum,less_num

def train_val_split(train,shop_info):
    validation = train[(train['time_stamp'] >= '2017-08-25 00:00:00')]
    # validation.reset_index(inplace=True)
    train = train[(train['time_stamp'] < '2017-08-25 00:00:00')]
    # train.reset_index(inplace=True)
    validation = pd.merge(validation, shop_info[['shop_id','mall_id']], on='shop_id', how='left')
    validation.rename(columns={'shop_id':'real_shop_id'},inplace=True)
    validation.loc[:,'label']=0
    validation.reset_index(inplace=True)
    validation.rename(columns={'index':'row_id'},inplace=True)#模拟测试集

    return train,validation

#重命名（为后续样本merge）
def rename(train,shop_info):
    shop_info.rename(columns={'longitude': 'longitude_shop','latitude':'latitude_shop'}, inplace=True)
    train = pd.merge(train, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train.reset_index(inplace=True)
    train.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集
    return train,shop_info

#建立按强度排序的dict
def get_wifi_dict_sorted(wifi_trian,wifi_test,wifi_validation,wifi_shop):
    wifi_train_dict = {}
    wifi_validation_dict = {}
    wifi_test_dict = {}
    wifi_shop_dict = {}
    for i in tqdm(range(wifi_trian.shape[0])):
        t=sorted(eval(wifi_trian[i, 1]).items(), key=lambda x: x[1], reverse=True)
        wifi_train_dict[wifi_trian[i, 0]] =list(map(lambda x:x[0],t))
    for i in tqdm(range(wifi_validation.shape[0])):
        t=sorted(eval(wifi_validation[i, 1]).items(), key=lambda x: x[1], reverse=True)
        wifi_validation_dict[wifi_validation[i, 0]] =list(map(lambda x:x[0],t))
    for i in tqdm(range(wifi_test.shape[0])):
        t=sorted(eval(wifi_test[i, 1]).items(), key=lambda x: x[1], reverse=True)
        wifi_test_dict[wifi_test[i, 0]] =list(map(lambda x:x[0],t))
    for i in tqdm(range(wifi_shop.shape[0])):
        t = sorted(eval(wifi_shop[i, 1]).items(), key=lambda x: x[1], reverse=True)
        wifi_shop_dict[wifi_shop[i, 0]] = list(map(lambda x:x[0],t))

    return wifi_train_dict,wifi_validation_dict,wifi_test_dict,wifi_shop_dict

#建立保留强度数值的dict
def get_wifi_dict_with_ssid(wifi_trian,wifi_test,wifi_validation,wifi_shop):
    wifi_train_dict = {}
    wifi_validation_dict = {}
    wifi_test_dict = {}
    wifi_shop_dict = {}
    for i in tqdm(range(wifi_trian.shape[0])):
        wifi_train_dict[wifi_trian[i, 0]] =eval(wifi_trian[i, 1])
    for i in tqdm(range(wifi_validation.shape[0])):
        wifi_validation_dict[wifi_validation[i, 0]] =eval(wifi_validation[i, 1])
    for i in tqdm(range(wifi_test.shape[0])):
        wifi_test_dict[wifi_test[i, 0]] =eval(wifi_test[i, 1])
    for i in tqdm(range(wifi_shop.shape[0])):
        wifi_shop_dict[wifi_shop[i, 0]] = eval(wifi_shop[i, 1])

    return wifi_train_dict, wifi_validation_dict, wifi_test_dict, wifi_shop_dict


def get_feature(train,wifi_shop_dict,wifi_train_dict,result):
    # #计算map排名score
    # ids=result[['row_id','shop_id']].values
    # mapk5=[]
    # mapk10=[]
    # for i in tqdm(range(ids.shape[0])):
    #     mapk5.append(apk(wifi_shop_dict[ids[i, 1]], wifi_train_dict[ids[i, 0]], k=5))
    #     mapk10.append(apk(wifi_shop_dict[ids[i, 1]], wifi_train_dict[ids[i, 0]], k=10))
    # result.loc[:, 'mapk5'] = mapk5
    # result.loc[:, 'mapk10'] = mapk10
    #
    # #用户访问次数
    # user_times=train.groupby(['user_id', 'shop_id'], as_index=False)['user_id'].agg({'user_times': 'count'})
    # result = pd.merge(result, user_times, on=['user_id', 'shop_id'], how='left')
    # result['user_times'].fillna(0, inplace=True)

    # 计算相同wifi平均强度差（强，弱）
    # 统计比均值强（弱）的wifi数量
    ids=result[['row_id','shop_id']].values
    large_wifi_sum=[]
    large_wifi_num=[]
    less_wifi_sum=[]
    less_wifi_num=[]
    for i in tqdm(range(ids.shape[0])):
        large_sum, large_num, less_sum, less_num=ssid_sub(wifi_shop_dict[ids[i, 1]], wifi_train_dict[ids[i, 0]])
        large_wifi_sum.append(large_sum)
        large_wifi_num.append(large_num)
        less_wifi_sum.append(less_sum)
        less_wifi_num.append(less_num)
    result.loc[:, 'large_wifi_sum'] = large_wifi_sum
    result.loc[:, 'large_wifi_num'] = large_wifi_num
    result.loc[:, 'less_wifi_sum'] = less_wifi_sum
    result.loc[:, 'less_wifi_num'] = less_wifi_num

    return result

df_train=pd.read_csv(train_path)
df_test=pd.read_csv(test_path)
df_shop_info=pd.read_csv(shop_path)
df_train,df_validation=train_val_split(df_train,df_shop_info)
df_train,df_shop_info=rename(df_train,df_shop_info)
wifi_trian = df_train[['row_id', 'wifi_dis']].values
wifi_validation=df_validation[['row_id', 'wifi_dis']].values
wifi_test=df_test[['row_id','wifi_dis']].values
wifi_shop = df_shop_info[['shop_id', 'wifi_avgdis_shop']].values

# #建立按强度排序的dict
# wifi_train_dict,wifi_validation_dict,wifi_test_dict,wifi_shop_dict\
#     =get_wifi_dict_sorted(wifi_trian,wifi_test,wifi_validation,wifi_shop)

#建立保留强度数值的dict
wifi_train_dict,wifi_validation_dict,wifi_test_dict,wifi_shop_dict\
    =get_wifi_dict_with_ssid(wifi_trian,wifi_test,wifi_validation,wifi_shop)

print('train feature:')
df_train_feat=pd.read_csv(train_feat_path)
df_train_feat=get_feature(df_train,wifi_shop_dict,wifi_train_dict,df_train_feat)
df_train_feat.to_csv(train_feat_path2,index=False)
del df_train_feat
gc.collect()
print('----------------------------------------------------')

print('validation feature:')
df_validation_feat=pd.read_csv(validation_feat_path)
df_validation_feat=get_feature(df_train,wifi_shop_dict,wifi_validation_dict,df_validation_feat)
df_validation_feat.to_csv(validation_feat_path2,index=False)
del df_validation_feat
gc.collect()
print('----------------------------------------------------')

print('test feature:')
df_test_feat=pd.read_csv(test_feat_path)
df_test_feat=get_feature(df_train,wifi_shop_dict,wifi_test_dict,df_test_feat)
df_test_feat.to_csv(test_feat_path2,index=False)
del df_test_feat
gc.collect()
print('----------------------------------------------------')