
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.File;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;


/**
 * 
 */

/**
 * @author SayanM
 *
 */
public class MainBDAS {
	
	public static class MapperBDAS extends Mapper<LongWritable, Text, Text, Text> {
		
		protected void map(LongWritable key, Text value, Context context)
				 throws IOException, InterruptedException {
			String classname = context.getConfiguration().get("classname");
			
			try {
				RootBDAS instance = (RootBDAS) Class.forName(classname).getConstructor().newInstance();
				String line = value.toString();
				HashMap<String, ArrayList<String>> result = instance.mapper_task(line);
				for(String k : result.keySet())
				{
					for(String v : result.get(k))
					{
						context.write(new Text(k), new Text(v));
					}
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} 
			
			
			}
				
	}
	
	public static class ReducerBDAS extends	 Reducer<Text, Text, Text, Text> {
		
		protected void reduce(Text key, Iterable<Text> values,
				 Context context) throws IOException, InterruptedException {
			String classname = context.getConfiguration().get("classname");
			
			try {
				RootBDAS instance = (RootBDAS) Class.forName(classname).getConstructor().newInstance();
				ArrayList<String> vals = new ArrayList<String>();
				for(Text v : values)
				{
					vals.add(v.toString());
				}
				HashMap<String, ArrayList<String>> result = instance.reducer_task(key.toString(), vals);
				for(String k : result.keySet())
				{
					for(String v : result.get(k))
					{
						context.write(new Text(k), new Text(v));
					}
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} 
			
		}
		
	}

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		Job job = new Job();
		 
		job.setJarByClass(MainBDAS.class);
		job.setJobName("MapReduceBDAS");
		 
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		 
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		 
	
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		job.setMapperClass(MapperBDAS.class);
		job.setReducerClass(ReducerBDAS.class);
		
		File file = new File("Config.xml");
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		Document doc = db.parse(file);
		doc.getDocumentElement().normalize();
		
		String classname = Utility.getClassName(doc);
		
		job.getConfiguration().set("classname", classname);
		 
		System.out.println(job.waitForCompletion(true));

	}

}
