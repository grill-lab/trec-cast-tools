package edu.gla.cast.search;

import com.google.common.base.Preconditions;
import org.lemurproject.galago.core.retrieval.ScoredDocument;
import org.lemurproject.galago.core.retrieval.query.Node;
import org.lemurproject.galago.core.retrieval.query.StructuredQuery;
import org.lemurproject.galago.utility.Parameters;
import org.lemurproject.galago.core.retrieval.Retrieval;
import org.lemurproject.galago.core.retrieval.RetrievalFactory;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class GalagoSimpleSearcher implements Searcher {

  private Retrieval m_retrieval;

  public GalagoSimpleSearcher(SearchConfiguration.Collection collection) throws Exception {
    Parameters globalParameters = Parameters.create();
    File indexDir = new File(collection.getLocation());
    Preconditions.checkArgument(indexDir.exists());
    globalParameters.set("index", collection.getLocation());
    globalParameters.putAll(collection.getGlobalParametersMap());
    m_retrieval = RetrievalFactory.create(globalParameters);
  }

  @Override
  public Search.SearchResults search(Search.SearchRequest searchRequest) throws Exception {
    Parameters queryParameters = Parameters.create();
    queryParameters.set("startAt", 0);
    // TODO: determine which is currently current in galago.
    queryParameters.set("resultCount", searchRequest.getParameters().getNumResults());
    queryParameters.set("requested", searchRequest.getParameters().getNumResults());
    queryParameters.putAll(searchRequest.getParameters().getParametersMap());
    Node parsedQuery = StructuredQuery.parse(searchRequest.getQuery());
    Node transformQuery = m_retrieval.transformQuery(parsedQuery, queryParameters);

    List<ScoredDocument> scoredDocuments = m_retrieval.executeQuery(transformQuery, queryParameters).scoredDocuments;
    if (scoredDocuments == null){
      scoredDocuments = new ArrayList();
    }

    // Note we're missing the text fields below.
    Search.SearchResults results = Search.SearchResults.newBuilder()
            .setRequest(searchRequest)
            .setHitCount(-1)
            .addAllResult(scoredDocuments.stream()
                    .map(result -> Search.ScoredResult.newBuilder()
                            .setId(result.getName())
                            .setScore(result.getScore())
                            .setRank(result.getRank())
                            .build()
                    ).collect(Collectors.toList()))
            .build();
    return results;
  }
}
