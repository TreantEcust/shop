package UDF;

import Base.BaseUDF;
import Utils.Imputer;
import Utils.Serializer;
import Utils.Sorted;
import Utils.Statistic;

import java.util.*;

/**
 * Created by wangdexun on 2017/11/25.
 * 将每条样本的wifi去重、均值并降序排列
 */
public class SampleWifiAggUDF extends BaseUDF {
    public String evaluate(String s, String how) {
        String[] wifiList = s.split(";");
        Map<String, List<Integer>> wifiMap = new HashMap<String, List<Integer>>();
        for (String wifiStr : wifiList) {
            String[] wifiInfo = wifiStr.split("\\|");
            // 处理wifi强度缺失值
            Imputer.fillNullInWifiInfo(wifiInfo);
            int strength = Integer.valueOf(wifiInfo[1]);
            if (wifiMap.containsKey(wifiInfo[0])) {
                wifiMap.get(wifiInfo[0]).add(strength);
            } else {
                List<Integer> strengthList = new ArrayList<Integer>();
                strengthList.add(strength);
                wifiMap.put(wifiInfo[0], strengthList);
            }
        }
        Map<String, Double> wifiAggMap = new HashMap<String, Double>();
        for (String key : wifiMap.keySet()) {
            if (how.equals("mean"))
                wifiAggMap.put(key, Statistic.mean(wifiMap.get(key)));
            else
                wifiAggMap.put(key, Double.valueOf(Statistic.max(wifiMap.get(key))));
        }
        // (降)排序
        List<Map.Entry<String, Double>> wifiAggList = Sorted.sort(wifiAggMap);
        // 返回结果
        return Serializer.serialize(wifiAggList);
    }
}
