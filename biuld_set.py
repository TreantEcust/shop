import pandas as pd
import numpy as np

count = 0


# 加入用户在train中去过的店铺作为负样本
def get_user_history(train, test):
    result = pd.merge(test, train, on='user_id', how='left')
    return result


# 获取目标点最近的N个店作为负样本
def get_nearest(shop_info, test):
    N = 10  # N近邻
    result = pd.merge(test, shop_info, on='mall_id', how='left')
    result.loc[:, 'simple_dis'] = abs(result['longitude_x'] - result['longitude_y']) + abs(
        result['latitude_x'] - result['latitude_y'])
    result.sort_values('simple_dis', inplace=True, ascending=False)
    result = result.groupby('row_id').tail(N)

    # 临时统计正确结果的覆盖率
    result.loc[:, 'label'] = (result['real_shop_id'] == result['shop_id'])
    ok = result['label'].values
    print(np.sum(ok) / (len(ok) / N))

    return result


def make(train, test, shop_info):
    print('构造负类样本...')
    user_history_shop = get_user_history(train, test)
    nearest_shop = get_nearest(shop_info, test)
