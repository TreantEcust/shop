import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import time

test_df = pd.read_csv('data/test_data.csv')
shop_df = pd.read_csv('data/shop_info.csv')
train_df = pd.read_csv('data/train_data.csv')

# #train分布
# x_train=train_df['longitude'].values
# y_train=train_df['latitude'].values
# y_train=y_train[np.where(x_train>60)[0]]
# x_train=x_train[np.where(x_train>60)[0]]
# x_train=x_train[np.where(y_train>20)[0]]
# y_train=y_train[np.where(y_train>20)[0]]
# plt.scatter(x_train,y_train,c='b')
# #test分布
# x_test=test_df['longitude'].values
# y_test=test_df['latitude'].values
# plt.scatter(x_test,y_test,c='r')
# plt.show()

# #统计冷启动用户
# user_in_test=test_df['user_id'].drop_duplicates().values
# user_in_train=train_df['user_id'].drop_duplicates().values
# user_without_records=0
# user_train_dict={}
# for u in user_in_train:
#     user_train_dict[u]=1
# for u in user_in_test:
#     if u not in user_train_dict:user_without_records+=1
# print("user_without_records:"+str(user_without_records)+'/'+str(len(user_in_test)))

# #统计消费时间
# train_time=train_df['time_stamp'].values
# train_time = list(map(lambda x: int(x.split(' ')[1].split(':')[0]), train_time))
# test_time=test_df['time_stamp'].values
# test_time = list(map(lambda x: int(x.split(' ')[1].split(':')[0]), test_time))
# plt.hist(x=pd.Series(train_time).dropna(), bins=50, facecolor='red', label='train_hour')
# plt.hist(x=pd.Series(test_time).dropna(), bins=50, facecolor='blue', label='test_hour')
# plt.legend()
# plt.show()

# #统计消费日期（决定验证集）
# train_time=train_df['time_stamp'].values
# train_time = list(map(lambda x: int(x.split(' ')[0].split('-')[2]), train_time))
# plt.hist(x=pd.Series(train_time).dropna(), bins=50, facecolor='red', label='date')
# plt.legend()
# plt.show()

# 统计商城内店的数量
# shop_count = shop_df.groupby('mall_id',as_index=False)['shop_id'].agg({'shop_count':'count'})['shop_count'].values

# # shop wifi地址统计
# def wifi_count(df_train):
#     dict_shop={}
#     N=-50
#     s_in_train=df_train['shop_id'].values
#     wifi_in_train=df_train['wifi_infos'].values
#     num_all=[]
#     for i,s in enumerate(s_in_train):
#         print(i)
#         if s not in dict_shop:
#             dict_shop[s]={}
#         w=wifi_in_train[i].split(';')
#         wifi_ssid=[]
#         wifi_dis=[]
#         wifi_bool=[]
#         for s in w:
#             infos=s.split('|')
#             wifi_ssid.append(infos[0])
#             wifi_dis.append(int(infos[1]))
#             wifi_bool.append(infos[2])
#         wifi_dis=np.array(wifi_dis)
#         num_all.append(len(np.nonzero(wifi_dis<N)[0]))
#     plt.hist(x=pd.Series(num_all).dropna(), bins=50, facecolor='red', label='num<-50')
#     plt.legend()
#     plt.show()
# shop_info=wifi_count(train_df)

# mall_df=shop_df[['shop_id','mall_id']]
# train_df=pd.merge(train_df,mall_df,on='shop_id',how='left')
# mall_count=train_df.groupby('mall_id',as_index=False)['mall_id'].agg({'mall_count':'count'})#max:m_1175
# countvalues=mall_count['mall_count'].values
# plt.hist(x=pd.Series(countvalues).dropna(), bins=50, facecolor='red', label='count')
# plt.legend()
# plt.show()

train_df=pd.merge(train_df,shop_df[['shop_id','mall_id']],on='shop_id',how='left')
train_df=train_df[(train_df['mall_id']=='m_6337')]
shops=list(set(train_df['shop_id'].values))
print('shop num:'+str(len(shops)))
train_df=train_df.groupby('user_id',as_index=False)['user_id'].agg({'hot':'count'})
train_df.sort_values('hot',inplace=True)
q=1


# wifi_dis=train_df['wifi_dis'].values
# wifi_dict={}
# for w in wifi_dis:
#     w=set(eval(w))
#     for s in w:
#         if s not in wifi_dict:
#             wifi_dict[s]=1
#         else:
#             wifi_dict[s]+=1
# temp=list(wifi_dict.values())
# plt.hist(x=pd.Series(temp).dropna(), bins=100, facecolor='red', label='count')
# plt.legend()
# plt.show()