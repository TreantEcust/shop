package MapReduce;

import MapReduce.WifiFeats.WifiApk;
import MapReduce.WifiFeats.WifiDiff;
import MapReduce.WifiFeats.WifiRFD;
import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Created by wangdexun on 2017/11/27.
 * Wi-Fi特征提取
 * rfd、large_sum、large_num、less_sum、less_num、apk
 */
public class WifiFeatsMapper extends MapperBase {

    private Record wifiFeats;

    @Override
    public void setup(TaskContext context) throws IOException {
        wifiFeats = context.createOutputRecord();
    }

    @Override
    // TODO Wi-Fi强度改成Integer节约存储空间
    public void map(long key, Record record, TaskContext context) throws IOException {
        wifiFeats.setBigint("no", record.getBigint(0));
        Map<String, Double> userWifiMap = wifiStrToMap(record.getString(1), null);
        Map<String, Double> shopWifiMap = wifiStrToMap(record.getString(2), userWifiMap);
        wifiFeats = WifiDiff.getInstance(userWifiMap, shopWifiMap).writeRecord(wifiFeats);
        wifiFeats = WifiRFD.getInstance(userWifiMap, shopWifiMap).writeRecord(wifiFeats);
        wifiFeats = WifiApk.getInstance(userWifiMap.keySet(), shopWifiMap.keySet(), 4).writeRecord(wifiFeats);
        wifiFeats = WifiApk.getInstance(userWifiMap.keySet(), shopWifiMap.keySet(), 10).writeRecord(wifiFeats);
        context.write(wifiFeats);
    }


    /**
     * 将wifi字符串转成(Linked)Map形式
     *
     * @param wifiStr    Wi-Fi字符串
     * @param anotherMap 求交集的另一个Map，减少内存使用
     * @return WifiMap
     */
    private Map<String, Double> wifiStrToMap(String wifiStr, Map<String, Double> anotherMap) {
        Map<String, Double> wifiMap = new LinkedHashMap<String, Double>();
        String[] wifiArray = wifiStr.split(",");
        String[] wifiInfo;
        for (String i : wifiArray) {
            wifiInfo = i.split(":");
            if (anotherMap == null || anotherMap.containsKey(wifiInfo[0]))
                wifiMap.put(wifiInfo[0], Double.valueOf(wifiInfo[1]));
            else
                wifiMap.put(wifiInfo[0], null);
        }
        return wifiMap;
    }

}
