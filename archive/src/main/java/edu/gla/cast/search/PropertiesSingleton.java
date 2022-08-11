package edu.gla.cast.search;

import com.google.protobuf.util.JsonFormat;

import java.io.IOException;
import java.net.URL;
import java.util.Scanner;


/**
 * PropertiesSingleton is a class which holds the data read from the configuration file.
 * The configuration may be reloaded, however some of the settings (such as server port) will not be
 * affected.
 */
public final class PropertiesSingleton {
  private static PropertiesSingleton _instance;
  private static SearchConfiguration.SearchConfig _searchConfig; // Protocol Buffer data structure holding all the data
  // read from the configuration file.

  public static synchronized SearchConfiguration.SearchConfig getConfig() {
    return _searchConfig;
  } // Get the CoreConfiguration instance with the data from config file.

  /**
   * Reload properties from a given configuration file.
   *
   * @param url - URL of the configuration file.
   * @throws IOException - Thrown, when there are problems with the URL or the file under
   *         the URL.
   */
  public static synchronized void reloadProperties(URL url) throws IOException {
    _instance = null;
    getPropertiesSingleton(url);
  }

  /**
   * Return the instance of this singleton.
   *
   * @param url - URL of the configuration file.
   * @throws IOException - Thrown, when there are problems with the URL or the file under
   *         the URL.
   */
  public static synchronized PropertiesSingleton getPropertiesSingleton(URL url) throws
          IOException {
    if (_instance == null) {
      _instance = new PropertiesSingleton();
      setProperties(url);
    }
    return _instance;
  }

  /**
   * Create an instance of CoreConfig class, which holds the data of a JSON configuration file
   * stored under the specified URL.
   *
   * @param url - URL of the configuration file.
   * @throws IOException - Thrown, when there are problems with the URL or the file under
   *         the URL.
   */
  private static void setProperties(URL url) throws IOException {
    SearchConfiguration.SearchConfig.Builder configBuilder = SearchConfiguration.SearchConfig.newBuilder();
    String jsonText = readPropertiesFromUrl(url);
    JsonFormat.parser().merge(jsonText, configBuilder);
    _searchConfig = configBuilder.build();
  }

  /**
   * Return a String of a JSON file stored under specified URL.
   *
   * @param url - URL of the configuration file.
   * @return - String holding the data from the JSON file specified by the provided URL.
   * @throws IOException - Thrown, when there are problems with the URL or the file under
   *         the URL.
   */
  private static String readPropertiesFromUrl(URL url) throws IOException {
    return new Scanner(url.openStream()).useDelimiter("\\Z").next();

  }
}

