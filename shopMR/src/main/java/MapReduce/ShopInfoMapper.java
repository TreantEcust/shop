package MapReduce;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import java.io.IOException;

/**
 * Created by wangdexun on 2017/11/26.
 * 计算商铺热度、商铺时间等
 */
public class ShopInfoMapper extends MapperBase {

    private Record mallId;
    private Record shopInfo;

    @Override
    public void setup(TaskContext context) throws IOException {
        mallId = context.createMapOutputKeyRecord();
        shopInfo = context.createMapOutputValueRecord();
    }

    @Override
    public void map(long key, Record record, TaskContext context) throws IOException {
        mallId.setString("mall_id", record.getString(5));
        shopInfo.setString("shop_id", record.getString(1));
        shopInfo.setDouble("time", record.getDouble(2));
        context.write(mallId, shopInfo);
    }
}
