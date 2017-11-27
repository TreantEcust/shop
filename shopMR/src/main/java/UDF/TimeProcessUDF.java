package UDF;

import Base.BaseUDF;

/**
 * Created by ewrfcas on 2017/11/22.
 * 将时间字符串转成分钟数
 */
public class TimeProcessUDF extends BaseUDF {
    public String evaluate(String s) {
        int hour = Integer.parseInt(s.split(" ")[1].split(":")[0]);
        int minutes = Integer.parseInt(s.split(" ")[1].split(":")[1]);
        return String.valueOf(hour * 60 + minutes);
    }
}