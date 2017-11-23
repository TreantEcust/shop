import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import java.io.IOException;
import java.util.Iterator;

/**
 * Created by wangdexun on 2017/11/23.
 * 计算每个mall的平均price
 */
public class MallAvgPriceReducer extends ReducerBase {
    private Record result;

    @Override
    public void setup(TaskContext context) throws IOException {
        result = context.createOutputRecord();
    }

    @Override
    public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {
        int sum = 0;
        int num = 0;
        while (values.hasNext()) {
            Record val = values.next();
            sum += val.getBigint("price");
            num += 1;
        }
        result.set("mall_id", key.get(0));
        result.set("price", sum * 1.0f / num);
        context.write(result);
    }
}
