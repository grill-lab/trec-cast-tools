package edu.gla.cast.search;

import java.io.IOException;
import java.util.Map;

/**
 * The manager is configured to setup searchers on the provided collections.
 */
public class SearchManager {

  // List of instances of searchers.
  private Map<String, Searcher> _searcher;

  private String defaultCollection;

   public void setupSearchers(SearchConfiguration.SearchConfig searchConfig) throws IllegalArgumentException, Exception {
     for (SearchConfiguration.Collection collection : searchConfig.getCollectionList()) {
       switch (collection.getType()) {
         // Add support for other collections below.
         case GALAGO:
           GalagoSimpleSearcher searcher = new GalagoSimpleSearcher(collection);
           _searcher.put(collection.getIdentifier(), searcher);
         default:
           throw new IllegalArgumentException("The type of the searcher provided " +
                   collection.getType().toString() + "\" is not supported (yet)!");
       }
     }
   }

   public edu.gla.cast.search.Search.SearchResults search(Search.SearchRequest request) throws IllegalArgumentException, Exception {
     String collection = request.getCollectionId();
     if (collection == null || collection.isEmpty()) {
       throw new IllegalArgumentException("collection must be specified for now.");
     }

     Searcher searcher = _searcher.get(request.getCollectionId());
     return searcher.search(request);
   }
}
