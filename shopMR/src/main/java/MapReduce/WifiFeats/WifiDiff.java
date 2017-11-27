package MapReduce.WifiFeats;

import Utils.Statistic;
import com.aliyun.odps.data.Record;

import java.util.Map;
import java.util.Set;

/**
 * Created by wangdexun on 2017/11/27.
 * large_sum large_num less_sum less_num
 */
public final class WifiDiff implements WifiFeat {

    private static volatile WifiDiff wifiDiff = null;
    private double largeSum;
    private double largeNum;
    private double lessSum;
    private double lessNum;


    public static WifiDiff getInstance(Map<String, Double> userWifiMap, Map<String, Double> shopWifiMap) {
        if (wifiDiff == null)
            wifiDiff = new WifiDiff();
        wifiDiff.reset();
        Set<String> interKeys = Statistic.intersection(userWifiMap.keySet(), shopWifiMap.keySet());
        for (String bssid : interKeys) {
            double strength1 = userWifiMap.get(bssid);
            double strength2 = shopWifiMap.get(bssid);
            if (strength1 >= strength2) {
                wifiDiff.largeSum += (strength1 - strength2);
                wifiDiff.largeSum += 1;
            } else {
                wifiDiff.lessSum += (strength2 - strength1);
                wifiDiff.lessNum += 1;
            }
            if (wifiDiff.largeNum > 0)
                wifiDiff.largeSum /= wifiDiff.largeNum;
            if (wifiDiff.lessNum > 0)
                wifiDiff.lessSum /= wifiDiff.lessNum;
        }
        return wifiDiff;
    }

    public Record writeRecord(Record record) {
        record.set("large_sum", largeSum);
        record.set("large_num", largeNum);
        record.set("less_sum", lessSum);
        record.set("less_num", lessNum);
        return record;
    }

    public void reset() {
        largeSum = 0;
        largeNum = 0;
        lessSum = 0;
        lessNum = 0;
    }
}
