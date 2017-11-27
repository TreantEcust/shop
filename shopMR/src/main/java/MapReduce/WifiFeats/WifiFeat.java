package MapReduce.WifiFeats;

import com.aliyun.odps.data.Record;

/**
 * Created by wangdexun on 2017/11/27.
 * 一梭才去一梭痴
 */
public interface WifiFeat {
    // 写入记录
    Record writeRecord(Record record);

    // 属性默认值
    void reset();
}
