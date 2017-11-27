package MapReduce.WifiFeats;

import com.aliyun.odps.data.Record;

import java.util.*;

/**
 * Created by wangdexun on 2017/11/27.
 * apk_4 apk_10
 */
public final class WifiApk implements WifiFeat {

    private static volatile WifiApk wifiApk = null;
    private double apk;
    private int k;

    public static WifiApk getInstance(Set<String> userWifiId, Set<String> shopWifiId, int k) {
        if (wifiApk == null)
            wifiApk = new WifiApk();
        wifiApk.k = k;
        List<String> userWifiIdTopK = topK(userWifiId, k);
        List<String> shopWifiIdTopK = topK(shopWifiId, k);
        if (shopWifiIdTopK.size() == 0) {
            wifiApk.reset();
            return wifiApk;
        }
        double score = 0;
        double hitsNum = 0;
        int i = 0;
        for (String id : userWifiIdTopK) {
            if (shopWifiIdTopK.contains(id)) {
                hitsNum += 1;
                score += hitsNum / (i + 1);
            }
            i++;
        }
        wifiApk.apk = score / shopWifiIdTopK.size();
        return wifiApk;
    }

    private static List<String> topK(Set<String> oldSet, int k) {
        List<String> newList;
        if (oldSet.size() > k) {
            newList = new ArrayList<String>();
            int count = 0;
            for (String i : oldSet) {
                newList.add(i);
                count++;
                if (count >= k)
                    break;
            }
        } else {
            newList = new ArrayList<String>(oldSet);
        }
        return newList;
    }


    public Record writeRecord(Record record) {
        record.set(String.format("apk_%d", k), apk);
        return record;
    }

    public void reset() {
        wifiApk.apk = 0;
    }
}
