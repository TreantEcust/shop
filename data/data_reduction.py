import pandas as pd
df=pd.read_csv('train_feat.csv')
df.drop(['wifi_dis','wifi_infos_shop'], axis=1, inplace=True)
df.to_csv('train_feat2.csv',index=False)

df=pd.read_csv('validation_feat.csv')
df.drop(['wifi_dis','wifi_infos_shop','wifi_infos'], axis=1, inplace=True)
df.to_csv('validation_feat2.csv',index=False)

df=pd.read_csv('test_feat.csv')
df.drop(['wifi_dis','wifi_infos_shop','wifi_infos'], axis=1, inplace=True)
df.to_csv('test_feat2.csv',index=False)

