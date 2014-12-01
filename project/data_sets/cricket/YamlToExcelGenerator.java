package cs586project.yamldatasetgenerator;

import java.io.File;
import java.io.FileInputStream;
import java.io.FilenameFilter;
import java.io.InputStream;
import java.util.Map;

import org.json.simple.JSONArray;
import org.yaml.snakeyaml.Yaml;

public class YamlToExcelGenerator {

	public static void main(String[] args) {
		
		try{
			JSONArray array = new JSONArray();
			FilenameFilter textFilter = new FilenameFilter() {
				public boolean accept(File dir, String name) {
					String lowercaseName = name.toLowerCase();
					if (lowercaseName.endsWith(".yaml")) {
						return true;
					} else {
						return false;
					}
				}
			};
			File directory = new File("/Users/abhisagrawal/Desktop/all");
			File[] files = directory.listFiles(textFilter);
			for(File f:files){
				InputStream input = new FileInputStream(f);
				Yaml yaml = new Yaml();
				Map obj = (Map)yaml.load(input);
				array.add(obj.get("info"));
			}
			System.out.println(array);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}
