package Utils;

import java.util.*;

/**
 * Created by wangdexun on 2017/11/26.
 */
public class Sorted {

    public static <T, R extends Comparable<R>> List<Map.Entry<T, R>> sort(Map<T, R> map) {
        List<Map.Entry<T, R>> map2List = new ArrayList<Map.Entry<T, R>>(map.entrySet());
        Collections.sort(map2List, new Comparator<Map.Entry<T, R>>() {
            public int compare(Map.Entry<T, R> o1, Map.Entry<T, R> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });
        return map2List;
    }
}
