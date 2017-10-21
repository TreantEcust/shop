import pandas as pd
import time
import numpy as np
import gc
import biuld_set
import biuld_feature
from tqdm import tqdm

train_path='../data/train_data.csv'
test_path='../data/test_data.csv'
shop_path='../data/shop_info.csv'


def train_val_split(train, shop_info):
    validation = train[(train['time_stamp'] >= '2017-08-25 00:00:00')]
    # validation.reset_index(inplace=True)
    train = train[(train['time_stamp'] < '2017-08-25 00:00:00')]
    # train.reset_index(inplace=True)
    validation = pd.merge(validation, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    validation.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    validation.loc[:, 'label'] = 0
    validation.reset_index(inplace=True)
    validation.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集

    return train, validation


def train_split(train, shop_info):
    np.random.seed(201708)
    # 随机挑选一些index
    train2_index = list(np.random.choice(np.arange(train.shape[0]), int(train.shape[0] / 10), replace=False))
    train1_index = list(set(np.arange(train.shape[0])).difference(train2_index))
    train1 = train.loc[train1_index]
    train2 = train.loc[train2_index]
    train1.dropna(axis=0, how='any',inplace=True)
    train2.dropna(axis=0, how='any',inplace=True)
    train2 = pd.merge(train2, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train2.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    train2.loc[:, 'label'] = 0
    train2.reset_index(inplace=True)
    train2.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集

    return train1, train2


#重命名（为后续样本merge）
def rename(train_b,train,shop_info):
    shop_info.rename(columns={'longitude': 'longitude_shop','latitude':'latitude_shop'}, inplace=True)
    train_b.rename(
        columns={'longitude': 'longitude_train', 'latitude': 'latitude_train', 'time_stamp': 'time_stamp_train'
            , 'wifi_dis': 'wifi_dis_train', 'wday': 'wday_train', 'minutes': 'minutes_train'}, inplace=True)
    train = pd.merge(train, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train_b = pd.merge(train_b, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    train.loc[:, 'label'] = 0
    train.reset_index(inplace=True)
    train.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集
    return train_b,train,shop_info

# 设置类标
def label_set(result):
    result.loc[:, 'label'] = (result['real_shop_id'] == result['shop_id']).astype('int')
    return result

if __name__ == "__main__":
    t0 = time.time()
    train = pd.read_csv(train_path)
    shop_info = pd.read_csv(shop_path)

    #delete info
    train.drop('wifi_infos', axis=1, inplace=True)
    print('分离训练，验证集')

    train,validation=train_val_split(train,shop_info)#train用于构造validation的特征
    train_b=train.copy()

    #原特征改名
    train_b,train,shop_info=rename(train_b,train,shop_info)

    #只选择m_1175的样本
    train=train[(train['mall_id']=='m_1175')]
    validation=validation[(validation['mall_id']=='m_1175')]
    shop_info=shop_info[(shop_info['mall_id']=='m_1175')]

    #label处理
    label_dict={}
    label_str=shop_info['shop_id'].values
    for i,l in enumerate(label_str):
        label_dict[l]=i
    label_temp=train['real_shop_id'].values
    labels=[]
    for l in label_temp:
        labels.append(label_dict[l])
    train.loc[:,'label']=labels
    label_temp = validation['real_shop_id'].values
    labels = []
    for l in label_temp:
        labels.append(label_dict[l])
    validation.loc[:,'label'] = labels

    #构造特征
    #wifi
    wifi_train=train['wifi_dis'].values
    wifi_train=list(map(lambda x:set(eval(x)),wifi_train))
    wifi_validation=validation['wifi_dis'].values
    wifi_validation=list(map(lambda x:set(eval(x)),wifi_validation))
    wifi_shop=shop_info['wifi_avgdis_shop'].values
    for i in tqdm(range(len(label_str))):
        #train
        w2=set(eval(wifi_shop[i]))
        wifi_inter=[]
        for w in wifi_train:
            wifi_inter.append(len(w&w2))
        train.loc[:,'wifi_'+label_str[i]]=wifi_inter
        #eval
        wifi_inter=[]
        for w in wifi_validation:
            wifi_inter.append(len(w&w2))
        validation.loc[:,'wifi_'+label_str[i]]=wifi_inter
    feat_columns=['longitude','latitude','minutes','wday']
    feat_columns.extend(list(map(lambda x:'wifi_'+x,label_str)))
    feat_columns.append('label')
    train=train[feat_columns]
    validation=validation[feat_columns]
    train.to_csv('train_feat.csv',index=False)
    validation.to_csv('validation_feat.csv',index=False)

