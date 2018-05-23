import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

/**
 * 
 */

/**
 * @author SayanM
 *
 */
public class Utility {
	
	public static String getClassName(Document doc)
	{
		NodeList nodeLst = doc.getElementsByTagName("ClassName");
		return nodeLst.item(0).getNodeValue();
	}

}
