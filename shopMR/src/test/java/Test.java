import Base.BaseUDF;
import MapReduce.ShopInfoMapper;
import Utils.Statistic;
import ch.hsr.geohash.GeoHash;

import java.util.*;

/**
 * Created by wangdexun on 2017/11/23.
 * 测试
 */
public class Test {
    public static void main(String[] args) {
//        System.out.println(GeoHash.geoHashStringWithCharacterPrecision(31.351320, 122.255867, 8));
//        System.out.println(new UDF.SampleWifiAggUDF().evaluate("b12|null|true;b13|-40|false;b11|-20|false;b11|-30|false", "mean"));
//        System.out.println(ShopInfoMapper.class.getName());
//        List<Integer> list=new ArrayList<Integer>();
//        list.add(5);
//        list.add(4);
//        list.add(3);
//        list.add(2);
//        list.add(0);
//        System.out.println(Statistic.median(list));
//        Set<String> s1=new HashSet<String>();
//        s1.add("wdx");
//        s1.add("gsj");
//        s1.add("wsj1");
//        Set<String> s2=new HashSet<String>();
//        s2.add("wdx");
//        s2.add("gsj1");
//        s2.add("wsj");
////        System.out.println(Statistic.union(s1,s2));
//        System.out.println(Math.pow(3,2));
        Map<String,Integer> map=new LinkedHashMap<String, Integer>();
        map.put("2",11);
        map.put("gsj",2);
        map.put("wdx2",13);
        map.put("3",3);
//        for(String key:map.keySet()){
//            System.out.println(map.get(key));
//        }
        System.out.println(new ArrayList<String>(map.keySet()));
//        double a=0;
//        System.out.println(a);
    }
}
