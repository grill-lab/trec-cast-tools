package edu.gla.cast.search;

public interface Searcher {

  Search.SearchResults search(Search.SearchRequest searchRequest) throws Exception;
}
