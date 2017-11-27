package MapReduce;

import Utils.Serializer;
import Utils.Sorted;
import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import java.io.IOException;
import java.util.*;

/**
 * Created by wangdexun on 2017/11/23.
 * 将每个shop的wifi记录整合，相同id求均值，再按照强度降序
 */
public class ShopWifiAggReducer extends ReducerBase {

    private Record result;

    @Override
    public void setup(TaskContext context) throws IOException {
        result = context.createOutputRecord();
    }

    @Override
    public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {
        Map<String, Integer> wifiCount = new HashMap<String, Integer>();
        Map<String, Long> strengthSum = new HashMap<String, Long>();
        Record record;
        String bssid;
        Long strength;
        while (values.hasNext()) {
            record = values.next();
            bssid = record.getString("bssid");
            strength = record.getBigint("strength");
            if (wifiCount.containsKey(bssid)) {
                wifiCount.put(bssid, wifiCount.get(bssid) + 1);
                strengthSum.put(bssid, strengthSum.get(bssid) + strength);
            } else {
                wifiCount.put(bssid, 1);
                strengthSum.put(bssid, strength);
            }
        }
        // 求均值or最大值
        // TODO Wi-Fi筛选策略
        Map<String, Double> strengthAvg = new HashMap<String, Double>();
        for (String id : wifiCount.keySet()) {
            if (wifiCount.get(id) >= 20) // 筛选
                strengthAvg.put(id, (double) (strengthSum.get(id) / wifiCount.get(id)));
        }
        if (strengthAvg.size() == 0) {
            System.out.println(String.format("%s店铺wifi频次很低...", key.getString("shop_id")));
            for (String id : wifiCount.keySet()) {
                strengthAvg.put(id, (double) (strengthSum.get(id) / wifiCount.get(id)));
            }
        }
        // 按照wifi强度降序排序
        List<Map.Entry<String, Double>> wifiList = Sorted.sort(strengthAvg);
        // 写入结果
        result.setString("shop_id", key.getString("shop_id"));
        result.setString("shop_agg_wifi", Serializer.serialize(wifiList));
        result.setBigint("wifi_count", (long) wifiList.size());
        context.write(result);
    }

}
