package UDF;

import Base.BaseUDF;
import ch.hsr.geohash.GeoHash;

/**
 * Created by wangdexun on 2017/11/24.
 */
public class LonLatGeohashUDF extends BaseUDF {
    public String evaluate(String lat, String lon, String precision) {
        return GeoHash.geoHashStringWithCharacterPrecision(Double.valueOf(lat), Double.valueOf(lon), Integer.valueOf(precision));
    }

}
