package MapReduce.WifiFeats;

import Utils.Statistic;
import com.aliyun.odps.data.Record;

import java.util.Map;
import java.util.Set;

/**
 * Created by wangdexun on 2017/11/27.
 * rfd1 rfd2
 * http://journals.sagepub.com/doi/full/10.1155/2015/109642#articleCitationDownloadContainer
 */
public final class WifiRFD implements WifiFeat {

    private static volatile WifiRFD wifiRFD = null;
    private double rfd1;
    private double rfd2;

    public static WifiRFD getInstance(Map<String, Double> userWifiMap, Map<String, Double> shopWifiMap) {
        if (wifiRFD == null)
            wifiRFD = new WifiRFD();
        wifiRFD.reset();
        Set<String> interKeys = Statistic.intersection(userWifiMap.keySet(), shopWifiMap.keySet());
        int interNum = interKeys.size();
        if (interNum > 0) {
            int unionNum = Statistic.union(userWifiMap.keySet(), shopWifiMap.keySet()).size();
            double jaccard = Math.log1p(interNum * 1. / unionNum);
            double l1 = 0, l2 = 0;
            for (String bssid : interKeys) {
                double strength1 = userWifiMap.get(bssid);
                double strength2 = shopWifiMap.get(bssid);
                l1 += Math.abs(strength1 - strength2);
                l2 += Math.pow(strength1 - strength2, 2);
            }
            int p = 1; // Jaccard系数
            wifiRFD.rfd1 = l1 / (interNum + p * jaccard);
            wifiRFD.rfd2 = Math.sqrt(l2) / (interNum + p * jaccard);
        }
        return wifiRFD;
    }

    public Record writeRecord(Record record) {
        record.set("rfd1", rfd1);
        record.set("rfd2", rfd2);
        return record;
    }

    public void reset() {
        // 最大距离
        rfd1 = 111111;
        rfd2 = 111111;
    }
}
