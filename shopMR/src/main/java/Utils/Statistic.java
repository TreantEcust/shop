package Utils;

import java.util.*;

/**
 * Created by wangdexun on 2017/11/25.
 * 常见的统计函数
 */
public class Statistic {

    public static <T extends Number> Double mean(List<T> list) {
        Double sum = 0.;
        for (T i : list) {
            sum += i.doubleValue();
        }
        return sum / list.size();
    }

    // TODO
    public static <T extends Number> Double median(List<T> list) {
        Collections.sort(list, new Comparator<T>() {
            public int compare(T o1, T o2) {
                return Double.compare(o1.doubleValue(), o2.doubleValue());
            }
        });
        int size = list.size();
        if (size % 2 == 0)
            return (list.get(size / 2 - 1).doubleValue() + list.get(size / 2).doubleValue()) / 2;
        return list.get(size / 2).doubleValue();
    }

    public static Integer max(List<Integer> list) {
        Integer max = -999;
        for (Integer i : list) {
            if (i > max) {
                max = i;
            }
        }
        return max;
    }

    public static <T> Set<T> intersection(Set<T> set1, Set<T> set2) {
        Set<T> interSet = new HashSet<T>();
        interSet.addAll(set1);
        interSet.retainAll(set2);
        return interSet;
    }

    public static <T> Set<T> union(Set<T> set1, Set<T> set2) {
        Set<T> unionSet = new HashSet<T>();
        unionSet.addAll(set1);
        unionSet.addAll(set2);
        return unionSet;
    }
}
