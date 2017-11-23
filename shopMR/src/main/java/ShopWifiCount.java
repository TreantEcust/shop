import com.aliyun.odps.udf.UDF;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by wangdexun on 2017/11/23.
 * 统计每条记录去重后的bssid数量
 */
public class ShopWifiCount extends UDF {
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
