package edu.gla.cast.search;

import com.google.protobuf.Timestamp;
import com.google.protobuf.util.JsonFormat;


import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.IOException;
import java.net.URL;
import java.time.Instant;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static com.google.common.base.Preconditions.checkNotNull;


  /**
   * The server which handles gRPC calls.
   */
  public class CastSearchServer {
    private final Server _server;
    private final 
    private static final Logger logger = LoggerFactory.getLogger(CastSearchServer.class);

    /**
     * Create a localhost server listening on specified port.
     *
     * @param port - the integer specifying the port.
     */
    public CastSearchServer(int port) {
      this(ServerBuilder.forPort(port));
    }

    /**
     * Create a localhost server listening on specified port.
     *
     * @param serverBuilder - the builder created for a particular port.
     */
    private CastSearchServer(ServerBuilder<?> serverBuilder) {
      _server = serverBuilder.addService(new CastSearchService()).build();
    }

    public static void main(String[] args) throws Exception {
      if (args == null || args.length == 0) {
        throw new Exception("Please specify the URL to the configuration file.");
      }
      logger.info("Loading config file from:" + args[0]);
      PropertiesSingleton.getPropertiesSingleton(new URL(args[0]));
      logger.info("Configuration loaded: " + PropertiesSingleton.getConfig().toString());
      CastSearchServer server = new CastSearchServer(PropertiesSingleton.getConfig()
              .getGrpcServerPort());
      server.start();
      server.blockUntilShutdown();
    }

    /**
     * Start the server.
     *
     * @throws IOException - Thrown when the server cannot start properly.
     */
    public void start() throws IOException {
      logger.info("Starting server");

      _server.start();
      logger.info("Started server.");
      Runtime.getRuntime().addShutdownHook(new Thread() {
        // In case the JVM is being shut down
        @Override
        public void run() {
          System.err.println("Server shut down due to JVM being shut down.");
          shutDown();
        }
      });
    }

    /**
     * Shut down the server.
     */
    public void shutDown() {
      logger.info("Shutting down server");

      if (_server != null) {
        _server.shutdown();
      }
    }

    /**
     * Wait until main thread is terminated. (gRPC is based on daemon threads)
     *
     * @throws InterruptedException
     */
    private void blockUntilShutdown() throws InterruptedException {
      if (_server != null) {
        _server.awaitTermination();
      }
    }

    /**
     * Serves the requests from clients/users.
     */
    static class CastSearchService extends CastSearchGrpc.CastSearchImplBase {

      /**
       * Sends the request to the agents and retrieves the chosen response.
       *
       * @param searchRequest    - The instance of the search request passed by the
       * @param responseObserver - The instance, which is used to pass the instance of
       *                         InteractionResponse with the response from the agents.
       */
      @Override
      public void getResponseFromAgents(Search.SearchRequest searchRequest,
                                        StreamObserver<Search.SearchResults> responseObserver) {
        try {
          String jsonString = JsonFormat.printer()
                  .preservingProtoFieldNames()
                  .print(searchRequest);

          logger.info("Processing request:" + jsonString);
        } catch (Exception e) {
          throw new IllegalArgumentException("Invalid protobuffer request!");
        }
        checkNotNull(searchRequest.getClientId(), "The SearchRequest doesn't have a client id!");

        try {
          searchManager.
        }

        Search.SearchResults results;
        Timestamp timestamp = Timestamp.newBuilder()
                .setSeconds(Instant.now()
                        .getEpochSecond())
                .setNanos(Instant.now()
                        .getNano())
                .build();
        try {
          response = dialogAgentManager.getResponse(interactionRequest);
          interactionResponse = InteractionResponse.newBuilder()
                  .setResponseId(response.getResponseId())
                  .setSessionId(dialogAgentManager.getSessionId())
                  .setTime(timestamp)
                  .setClientId(response.getClientId())
                  .setUserId(interactionRequest.getUserId())
                  .setMessageStatus(ClientMessageStatus.SUCCESSFUL)
                  .addAllInteraction(response.getActionList().stream()
                          .map(action -> action.getInteraction())
                          .collect(Collectors.toList()))
                  .build();
        } catch (Exception exception) {
          logger.warn("Error processing request :" + exception.getMessage() + " " + exception.getMessage());

          interactionResponse = InteractionResponse.newBuilder()
                  .setMessageStatus(InteractionResponse.ClientMessageStatus.ERROR)
                  .setErrorMessage(exception.getMessage())
                  .setTime(timestamp)
                  .build();
        }
        responseObserver.onNext(interactionResponse);
        responseObserver.onCompleted();
      }
    }
  }