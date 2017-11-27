package UDF;

import Base.BaseUDF;

/**
 * Created by ewrfcas on 2017/11/22.
 * 计算两点之间经纬度距离
 */
public class DisCalculateUDF extends BaseUDF {
    public String evaluate(String x1, String y1, String x2, String y2) {
        Double lon1 = Double.parseDouble(x1);
        Double lat1 = Double.parseDouble(y1);
        Double lon2 = Double.parseDouble(x2);
        Double lat2 = Double.parseDouble(y2);
        Double dx = Math.abs(lon1 - lon2);  // 经度差
        Double dy = Math.abs(lat1 - lat2);  // 维度差
        Double b = (lat1 + lat2) / 2.0;
        Double Lx = 6371004.0 * (dx / 57.2958) * Math.cos(b / 57.2958);
        Double Ly = 6371004.0 * (dy / 57.2958);
        Double L = Math.sqrt(Lx * Lx + Ly * Ly);
        return String.valueOf(L);
    }
}
