package MapReduce;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;


import java.io.IOException;

/**
 * Created by wangdexun on 2017/11/23.
 * 统计每个mall的平均price（目前没用）
 */
public class MallAvgPriceDriver {

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException, OdpsException {
        JobConf job = new JobConf();
        job.setMapOutputKeySchema(SchemaUtils.fromString("mall_id:string"));
        job.setMapOutputValueSchema(SchemaUtils.fromString("price:bigint"));
        InputUtils.addTable(TableInfo.builder().tableName(args[0]).build(), job);
        OutputUtils.addTable(TableInfo.builder().tableName(args[1]).build(), job);
        job.setMapperClass(MallAvgPriceMapper.class);
        job.setReducerClass(MallAvgPriceReducer.class);
        RunningJob rj = JobClient.runJob(job);
        rj.waitForCompletion();
    }
}
