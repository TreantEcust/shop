import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import java.io.IOException;

/**
 * Created by wangdexun on 2017/11/23.
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
        shopId.setString("shop_id", record.getString(1));
        String[] wifiArray = record.getString(5).split(";");
        for (String wifiStr : wifiArray) {
            String[] wifi = wifiStr.split("\\|");
            if (!wifi[1].equals("null")) {
                wifiInfo.setString("bssid", wifi[0]);
                wifiInfo.setBigint("strength", Long.valueOf(wifi[1]));
                context.write(shopId, wifiInfo);
            }
        }
    }
}
