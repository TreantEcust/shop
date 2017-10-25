#对multi_data中的feat文件的特征进行增删
import pandas as pd

#remove feat
def feat_remove(data,feat_list,path):
    data.drop(feat_list, axis=1, inplace=True)
    data.to_csv(path,index=False)

shop_path='../data/shop_info.csv'
shop_info = pd.read_csv(shop_path)
mall_list=list(set(shop_info['mall_id'].values))
shop_ids=shop_info[['mall_id','shop_id']]
for i,m in enumerate(mall_list):
    print(i)
    shop_info_temp=shop_ids[(shop_ids['mall_id']==m)]
    feat_drop = (list(map(lambda x: 'jac_' + x, shop_info_temp['shop_id'].values)))
    save_path='multi_data/'+m
    train_feat=pd.read_csv(save_path+'/train_feat.csv')
    feat_remove(train_feat,feat_drop,save_path+'/train_feat.csv')
    validation_feat=pd.read_csv(save_path+'/validation_feat.csv')
    feat_remove(validation_feat,feat_drop,save_path+'/validation_feat.csv')
    test_feat=pd.read_csv(save_path+'/test_feat.csv')
    feat_remove(test_feat,feat_drop,save_path+'/test_feat.csv')