import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import java.io.IOException;
import java.util.*;

/**
 * Created by wangdexun on 2017/11/23.
 * 统计每个shop所对应的wifi数量
 */
public class ShopWifiCountReducer extends ReducerBase {

    private Record result;

    @Override
    public void setup(TaskContext context) throws IOException {
        result = context.createOutputRecord();
    }

    @Override
    public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {
        Map<String, Integer> wifiCount = new HashMap<String, Integer>();
        Record record;
        String bssid;
        while (values.hasNext()) {
            record = values.next();
            bssid = record.getString("bssid");
            if (!wifiCount.containsKey(bssid)) {
                wifiCount.put(bssid, 1);
            }
        }
        // 写入结果
        result.setString("shop_id", key.getString("shop_id"));
        result.setBigint("wifi_count", (long) wifiCount.keySet().size());
        context.write(result);
    }
}
