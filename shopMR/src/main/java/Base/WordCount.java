///**
// * Created by wangdexun on 2017/11/23.
// */
//
//import org.apache.hadoop.conf.Configuration;
//import org.apache.hadoop.fs.FileSystem;
//import org.apache.hadoop.fs.Path;
//import org.apache.hadoop.io.IntWritable;
//import org.apache.hadoop.io.LongWritable;
//import org.apache.hadoop.io.Text;
//import org.apache.hadoop.mapreduce.Job;
//import org.apache.hadoop.mapreduce.Mapper;
//import org.apache.hadoop.mapreduce.Reducer;
//import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
//import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
//
//import java.io.IOException;
//import java.util.StringTokenizer;
//
//public class WordCount {
//
//    public static class TokenizerMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
//        private final static IntWritable one = new IntWritable(1);
//        private Text word = new Text();
//
//        @Override
//        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
//            StringTokenizer itr = new StringTokenizer(value.toString());
//            while (itr.hasMoreTokens()) {
//                word.set(itr.nextToken());
//                context.write(word, one);
//            }
//        }
//    }
//
//    public static class IntSumRecuder extends Reducer<Text, IntWritable, Text, IntWritable> {
//        private IntWritable result = new IntWritable();
//
//        @Override
//        protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
//            int sum = 0;
//            for (IntWritable i : values) {
//                sum += i.get();
//            }
//            result.set(sum);
//            context.write(key, result);
//        }
//    }
//
//    public static void Main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
//        Configuration conf = new Configuration();
//        Job job = Job.getInstance(conf, "word count");
//        job.setJarByClass(WordCount.class);
//        job.setMapperClass(TokenizerMapper.class);
//        job.setReducerClass(IntSumRecuder.class);
//        job.setOutputKeyClass(Text.class);
//        job.setOutputValueClass(IntWritable.class);
//        FileInputFormat.addInputPath(job, new Path(args[0]));
//        FileOutputFormat.setOutputPath(job, new Path(args[1]));
//        Path outputPath = new Path(args[1]);
//        FileSystem fs = FileSystem.get(conf);
//        if (fs.exists(outputPath)) {
//            fs.delete(outputPath, true);
//        }
//        job.waitForCompletion(true);
//    }
//}
