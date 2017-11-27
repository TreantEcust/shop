package Utils;

/**
 * Created by wangdexun on 2017/11/25.
 * 处理缺失值
 */
public class Imputer {

    public static void fillNullInWifiInfo(String[] wifiInfo) {
        /*
          处理wifi强度缺失值
         */
        if (wifiInfo[1].equals("null")) {
            if (wifiInfo[2].equals("true")) {
                wifiInfo[1] = "-50";
            } else {
                wifiInfo[1] = "-70";
            }
        }
    }
}
