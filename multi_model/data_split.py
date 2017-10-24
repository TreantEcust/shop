import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from sklearn.feature_extraction import DictVectorizer

train_path='../data/train_data.csv'
test_path='../data/test_data.csv'
shop_path='../data/shop_info.csv'
pd.options.mode.chained_assignment = None  # default='warn'
def train_val_split(train, shop_info):
    validation = train[(train['time_stamp'] >= '2017-08-25 00:00:00')]
    train = train[(train['time_stamp'] < '2017-08-25 00:00:00')]
    validation = pd.merge(validation, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    validation.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    validation.loc[:, 'label'] = 0
    validation.reset_index(inplace=True)
    validation.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集

    return train, validation

#重命名（为后续样本merge）
def rename(train,shop_info):
    shop_info.rename(columns={'longitude': 'longitude_shop','latitude':'latitude_shop'}, inplace=True)
    train = pd.merge(train, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    train.loc[:, 'label'] = 0
    train.reset_index(inplace=True)
    train.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集
    return train,shop_info

train = pd.read_csv(train_path)
shop_info = pd.read_csv(shop_path)
test=pd.read_csv(test_path)
mall_list=list(set(shop_info['mall_id'].values))

#delete info
train.drop('wifi_infos', axis=1, inplace=True)
train,validation=train_val_split(train,shop_info)#train用于构造validation的特征
#原特征改名
train,shop_info=rename(train,shop_info)

for i in tqdm(range(len(mall_list))):
    mall_id=mall_list[i]
    save_path='multi_data/'+mall_id
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    #train
    train_temp = train[(train['mall_id'] == mall_id)]
    validation_temp = validation[(validation['mall_id'] == mall_id)]
    test_temp=test[(test['mall_id']==mall_id)]
    shop_info_temp = shop_info[(shop_info['mall_id'] == mall_id)]

    # label处理
    label_dict = {}
    label_str = shop_info_temp['shop_id'].values
    for i, l in enumerate(label_str):
        label_dict[l] = i
    label_temp = train_temp['real_shop_id'].values
    labels = []
    for l in label_temp:
        labels.append(label_dict[l])
    train_temp.loc[:, 'label'] = labels
    label_temp = validation_temp['real_shop_id'].values
    labels = []
    for l in label_temp:
        labels.append(label_dict[l])
    validation_temp.loc[:, 'label'] = labels
    label_mapping=pd.DataFrame([list(label_dict.keys()),list(label_dict.values())],index=['shop_id','label'])
    label_mapping=label_mapping.transpose()
    label_mapping.to_csv(save_path+'/label_mapping.csv',index=False)

    # 构造特征
    # ssid
    wifi_train = train_temp['wifi_dis'].values
    wifi_train = list(map(lambda x: eval(x), wifi_train))
    vec = DictVectorizer()
    vec.fit_transform(wifi_train)
    ssid_names = vec.get_feature_names()

    wifi_train_df = pd.DataFrame(vec.transform(wifi_train).toarray(), columns=ssid_names)

    wifi_validation = validation_temp['wifi_dis'].values
    wifi_validation = list(map(lambda x: eval(x), wifi_validation))
    wifi_validation_df = pd.DataFrame(vec.transform(wifi_validation).toarray(), columns=ssid_names)

    wifi_test = test_temp['wifi_dis'].values
    wifi_test = list(map(lambda x: eval(x), wifi_test))
    wifi_test_df = pd.DataFrame(vec.transform(wifi_test).toarray(), columns=ssid_names)

    columns_names = list(train_temp.columns)
    columns_names.extend(ssid_names)
    columns_names_test=list(test_temp.columns)
    columns_names_test.extend(ssid_names)
    train_temp = pd.DataFrame(np.concatenate((np.array(train_temp), np.array(wifi_train_df)), axis=1),columns=columns_names)
    validation_temp = pd.DataFrame(np.concatenate((np.array(validation_temp), np.array(wifi_validation_df)), axis=1),columns=columns_names)
    test_temp = pd.DataFrame(np.concatenate((np.array(test_temp), np.array(wifi_test_df)), axis=1),columns=columns_names_test)

    wifi_train = list(map(lambda x: set(x), wifi_train))
    wifi_validation = list(map(lambda x: set(x), wifi_validation))
    wifi_test = list(map(lambda x: set(x), wifi_test))
    wifi_shop = shop_info_temp['wifi_avgdis_shop'].values
    for i in range(len(label_str)):
        w2 = set(eval(wifi_shop[i]))
        # train
        wifi_inter = []
        for w in wifi_train:
            wifi_inter.append(len(w & w2))
        train_temp.loc[:, 'wifi_' + label_str[i]] = wifi_inter
        # eval
        wifi_inter = []
        for w in wifi_validation:
            wifi_inter.append(len(w & w2))
        validation_temp.loc[:, 'wifi_' + label_str[i]] = wifi_inter
        #test
        wifi_inter = []
        for w in wifi_test:
            wifi_inter.append(len(w & w2))
        test_temp.loc[:, 'wifi_' + label_str[i]] = wifi_inter
    feat_columns = ['longitude', 'latitude', 'minutes', 'wday']
    feat_columns.extend(ssid_names)
    feat_columns.extend(list(map(lambda x: 'wifi_' + x, label_str)))
    feat_columns_test=feat_columns.copy()
    feat_columns_test.append('row_id')
    test_temp = test_temp[feat_columns_test]
    feat_columns.append('label')
    train_temp = train_temp[feat_columns]
    validation_temp = validation_temp[feat_columns]
    train_temp.to_csv(save_path+'/train_feat.csv', index=False)
    validation_temp.to_csv(save_path+'/validation_feat.csv', index=False)
    test_temp.to_csv(save_path+'/test_feat.csv', index=False)


