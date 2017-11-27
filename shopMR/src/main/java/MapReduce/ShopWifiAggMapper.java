package MapReduce;

import Utils.Imputer;
import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import java.io.IOException;

/**
 * Created by wangdexun on 2017/11/23.
 * 将每个shop的wifi记录整合，相同id求均值，再按照强度降序
 */
public class ShopWifiAggMapper extends MapperBase {

    private Record shopId;
    private Record wifiInfo;

    @Override
    public void setup(TaskContext context) throws IOException {
        shopId = context.createMapOutputKeyRecord();
        wifiInfo = context.createMapOutputValueRecord();
    }

    @Override
    public void map(long key, Record record, TaskContext context) throws IOException {
        // 判断日期
        String[] time_stamp = record.getString(2).split(" ")[0].split("-");
        if (Integer.valueOf(time_stamp[1]) == 8 && Integer.valueOf(time_stamp[2]) >= 20)
            return;
        shopId.setString("shop_id", record.getString(1));
        String[] wifiArray = record.getString(5).split(";");
        for (String wifiStr : wifiArray) {
            String[] wifi = wifiStr.split("\\|");
            Imputer.fillNullInWifiInfo(wifi);
            wifiInfo.setString("bssid", wifi[0]);
            wifiInfo.setBigint("strength", Long.valueOf(wifi[1]));
            context.write(shopId, wifiInfo);
        }
    }
}
