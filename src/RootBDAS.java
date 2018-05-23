import java.util.ArrayList;
import java.util.HashMap;

/**
 * 
 */

/**
 * @author SayanM
 *
 */
public abstract class RootBDAS {
	abstract  HashMap<String, ArrayList<String>>  mapper_task(String line);
	abstract  HashMap<String, ArrayList<String>>  reducer_task(String key, ArrayList<String> values);

}
