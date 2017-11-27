package Utils;

import java.util.List;
import java.util.Map;

/**
 * Created by wangdexun on 2017/11/26.
 * 序列化
 */
public class Serializer {

    public static <T, R> String serialize(List<Map.Entry<T, R>> mapList) {
        if (mapList == null || mapList.size() == 0)
            return "";
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<T, R> i : mapList) {
            builder.append(i.getKey());
            builder.append(":");
            builder.append(i.getValue());
            builder.append(",");
        }
        builder.deleteCharAt(builder.length() - 1);
        return builder.toString();
    }
}
