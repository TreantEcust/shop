import pandas as pd
import numpy as np
import time

# 时间处理
def process_time(train):
    print('时间处理...')
    st_times = list(train['time_stamp'].values)
    if np.nan in st_times:
        st_times.remove(np.nan)
    st_times = list(map(lambda x: time.strptime(x.split('.')[0], '%Y-%m-%d %H:%M'), st_times))
    time_min = []
    time_day = []
    #工作日是1，周末是0
    for timet in st_times:
        if timet.tm_wday==0 or timet.tm_wday==6:
            time_day.append(0)
        else:
            time_day.append(1)
        time_min.append(timet.tm_hour * 60 + timet.tm_min)
    train.loc[:, 'minutes'] = time_min
    train.loc[:, 'wday'] = time_day

    return train

train_path='训练数据-ccf_first_round_user_shop_behavior.csv'
test_path='AB榜测试集-evaluation_public.csv'
shop_path='训练数据-ccf_first_round_shop_info.csv'
#时间处理
df_train=pd.read_csv(train_path)
df_train=process_time(df_train)
df_train.to_csv('train_data.csv',index=False)

df_test=pd.read_csv(test_path)
df_test=process_time(df_test)
df_test.to_csv('test_data.csv',index=False)
