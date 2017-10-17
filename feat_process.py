import pandas as pd

train_path='data/train_feat2.csv'
test_path='data/test_feat2.csv'
validation_path='data/validation_feat2.csv'

train_path2='data/train_feat3.csv'
test_path2='data/test_feat3.csv'
validation_path2='data/validation_feat3.csv'

def nor_process(result,predictors):
    #candidate
    cand_num=result.groupby('row_id', as_index=False)['row_id'].agg({'cand_num': 'count'})
    result=pd.merge(result, cand_num, on='row_id', how='left')

    for p in predictors:
        print(p)
        temp_max = result.groupby('row_id', as_index=False)[p].agg({'max' + p: 'max'})
        temp_min = result.groupby('row_id', as_index=False)[p].agg({'min' + p: 'min'})
        result = pd.merge(result, temp_max, on='row_id', how='left')
        result = pd.merge(result, temp_min, on='row_id', how='left')
        result[p]=(result[p]-result['min'+p])/(result['max'+p]-result['min'+p]+0.0001)
        result.drop(['max'+p,'min'+p],inplace=True,axis=1)

    return result


predictors = ['user_shopmall','minutes','wifi_count','user_shop_times',
              'is_wday','user_mall_times','dis_shop','hot_point']

df=nor_process(pd.read_csv(validation_path),predictors)
df.to_csv(validation_path2,index=False)
df=nor_process(pd.read_csv(train_path),predictors)
df.to_csv(train_path2,index=False)
df=nor_process(pd.read_csv(test_path),predictors)
df.to_csv(test_path2,index=False)