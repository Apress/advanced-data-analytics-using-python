import java.util.ArrayList;
import java.util.HashMap;

/**
 * 
 */

/**
 * @author SayanM
 *
 */


public final class WordCounterBDAS extends RootBDAS{

	@Override
	HashMap<String, ArrayList<String>> mapper_task(String line) {
		// TODO Auto-generated method stub
		String[] words = line.split(" ");
		HashMap<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>>();
		for(String w : words)
		{
			if(result.containsKey(w))
			{
				ArrayList<String> vals = result.get(w);
				vals.add("1");
				result.put(w, vals);
			}
			else
			{
				ArrayList<String> vals = new ArrayList<String>();
				vals.add("1");
				result.put(w, vals);
			}
		}
		return result;
	}

	@Override
	HashMap<String, ArrayList<String>> reducer_task(String key, ArrayList<String> values) {
		// TODO Auto-generated method stub
		HashMap<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>>();
		ArrayList<String> tempres = new ArrayList<String>();
		tempres.add(values.size()+ "");
		result.put(key, tempres);
		return result;
	}

}
