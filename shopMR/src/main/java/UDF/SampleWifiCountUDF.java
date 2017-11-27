package UDF;

import Base.BaseUDF;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by wangdexun on 2017/11/23.
 * 统计每条样本去重后的bssid数量
 */
public class SampleWifiCountUDF extends BaseUDF {
    public String evaluate(String s) {
        String[] wifiArray = s.split(";");
        Map<String, Integer> wifiCount = new HashMap<String, Integer>();
        for (String wifiStr : wifiArray) {
            String bssid = wifiStr.split("\\|")[0];
            wifiCount.put(bssid, 1);
        }
        return String.valueOf(wifiCount.keySet().size());
    }
}
