package MapReduce;

import Utils.Statistic;
import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import java.io.IOException;
import java.util.*;

/**
 * Created by wangdexun on 2017/11/26.
 * 计算商铺热度、商铺时间等
 */
public class ShopInfoReducer extends ReducerBase {
    private Record result;

    @Override
    public void setup(TaskContext context) throws IOException {
        result = context.createOutputRecord();
    }

    @Override
    public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {
        Map<String, Integer> shopCount = new HashMap<String, Integer>();
        Map<String, List<Double>> shopTime = new HashMap<String, List<Double>>();
        Record record;
        int mallCount = 0;
        while (values.hasNext()) {
            record = values.next();
            String shopId = record.getString("shop_id");
            Double time = record.getDouble("time");
            if (shopCount.containsKey(shopId)) {
                shopCount.put(shopId, shopCount.get(shopId) + 1);
                shopTime.get(shopId).add(time);
            } else {
                shopCount.put(shopId, 1);
                List<Double> timeList = new ArrayList<Double>();
                timeList.add(time);
                shopTime.put(shopId, timeList);
            }
            mallCount++;
        }
        for (String shopId : shopCount.keySet()) {
            result.set("shop_id", shopId);
            result.set("shop_heat", shopCount.get(shopId) * 1. / mallCount);// 归一化热度
            result.set("shop_time_mean", Statistic.mean(shopTime.get(shopId)));// 平均消费时间
            result.set("shop_time_median", Statistic.median(shopTime.get(shopId)));// 中位数消费时间
            context.write(result);
        }
    }
}
