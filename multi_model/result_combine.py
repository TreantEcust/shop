import pandas as pd

shop_path='../data/shop_info.csv'
shop_info = pd.read_csv(shop_path)
mall_list=list(set(shop_info['mall_id'].values))
results=[]
for i,m in enumerate(mall_list):
    save_path='multi_data/'+m
    print('mall_id:' + m + ' (' + str(i + 1) + '/' + str(len(mall_list)) + ')')
    result=pd.read_csv(save_path+'/result.csv')
    results.append(result)
results=pd.concat(results,axis=0)
results.rename(columns={'shop_ids': 'shop_id'}, inplace=True)
results.to_csv('result.csv',index=False)
