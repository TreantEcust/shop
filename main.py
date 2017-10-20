import pandas as pd
import time
import numpy as np
import gc
import biuld_set

train_path = 'data/训练数据-ccf_first_round_user_shop_behavior.csv'
test_path = 'data/AB榜测试集-evaluation_public.csv'
shop_path = 'data/训练数据-ccf_first_round_shop_info.csv'


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
    train1.dropna(axis=0, how='any', inplace=True)
    train2.dropna(axis=0, how='any', inplace=True)
    train2 = pd.merge(train2, shop_info[['shop_id', 'mall_id']], on='shop_id', how='left')
    train2.rename(columns={'shop_id': 'real_shop_id'}, inplace=True)
    train2.loc[:, 'label'] = 0
    train2.reset_index(inplace=True)
    train2.rename(columns={'index': 'row_id'}, inplace=True)  # 模拟测试集

    return train1, train2


if __name__ == "__main__":
    t0 = time.time()
    train = pd.read_csv(train_path)
    shop_info = pd.read_csv(shop_path)

    print('分离训练，验证集')
    train, validation = train_val_split(train, shop_info)  # train用于构造validation的特征
    train1, train2 = train_split(train, shop_info)  # train1用于构造train2的特征

    print('构造训练集')
    train_feat = biuld_set.make(train1, train2, shop_info)
    train_feat.to_csv('data/train_feat.csv')
    del train1, train2, train_feat
    gc.collect()

    print('构造验证集')
    validation_feat = biuld_set.make(train, validation, shop_info)
    validation_feat.to_csv('data/validation_feat.csv')
    print('一共用时{}秒'.format(time.time() - t0))
