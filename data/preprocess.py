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

def process_wifi(train):
    print('处理wifi...')
    wifi_infos=list(train['wifi_infos'].values)
    if np.nan in wifi_infos:
        wifi_infos.remove(np.nan)
    wifi_dis=[]
    for w in wifi_infos:
        w2=w.split(';')
        wifi_dis_detail={}
        for wifi_detail in w2:
            w3=wifi_detail.split('|')
            wifi_dis_detail[w3[0]]=float(w3[1])
        wifi_dis.append(wifi_dis_detail)
    train.loc[:,'wifi_dis']=wifi_dis

    return train

def set_wifi(x,dict_counts_shop,dict_avgdis_shop):
    x['wifi_counts_shop']=str(dict_counts_shop[x[0]])
    x['wifi_avgdis_shop']=str(dict_avgdis_shop[x[0]])
    return x

# shop wifi地址统计
def wifi_count(shop_info,df_train):
    dict_counts_shop={}
    dict_avgdis_shop={}
    limit=-60
    s_in_train=df_train['shop_id'].values
    wifi_in_train=df_train['wifi_infos'].values
    for i,s in enumerate(s_in_train):
        # if i>50000:
        #     break
        print(i)
        if s not in dict_counts_shop:
            dict_counts_shop[s]={}
            dict_avgdis_shop[s]={}
        w=wifi_in_train[i].split(';')
        wifi_ssid=[]
        wifi_dis=[]
        for ss in w:
            infos=ss.split('|')
            wifi_ssid.append(infos[0])
            wifi_dis.append(int(infos[1]))
        wifi_ssid=np.array(wifi_ssid)
        wifi_dis=np.array(wifi_dis)
        add_index=np.where(wifi_dis>limit)[0]
        wifi_ssid=wifi_ssid[add_index]
        wifi_dis=wifi_dis[add_index]
        for j,wi in enumerate(wifi_ssid):
            if wi not in dict_counts_shop[s]:
                dict_counts_shop[s][wi]=1
                dict_avgdis_shop[s][wi]=wifi_dis[j]
            else:
                dict_counts_shop[s][wi]+=1
                dict_avgdis_shop[s][wi]+= wifi_dis[j]
    for k1 in dict_avgdis_shop:
        for k2 in dict_avgdis_shop[k1]:
            dict_avgdis_shop[k1][k2]/=dict_counts_shop[k1][k2]
    shop_info.loc[:,'wifi_counts_shop']=0
    shop_info.loc[:, 'wifi_avgdis_shop'] = 0
    shop_info=shop_info.apply(lambda x:set_wifi(x,dict_counts_shop,dict_avgdis_shop),axis=1)

    return shop_info

train_path='训练数据-ccf_first_round_user_shop_behavior.csv'
test_path='AB榜测试集-evaluation_public.csv'
shop_path='训练数据-ccf_first_round_shop_info.csv'
#时间处理
df_train=pd.read_csv(train_path)
df_train=process_time(df_train)
df_train=process_wifi(df_train)
df_train.to_csv('train_data.csv',index=False)

df_test=pd.read_csv(test_path)
df_test=process_time(df_test)
df_test=process_wifi(df_test)
df_test.to_csv('test_data.csv',index=False)

#shop wifi统计
# shop_info=pd.read_csv(shop_path)
# shop_info=wifi_count(shop_info,df_train)
# shop_info.to_csv('shop_info.csv',index=False)
