package edu.gla.cast;

import cast.topics.TopicDef;
import cast.topics.TopicDef.Topic;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Read in a topic text file encoded in:
 *
 * A text file has the format:
 * Number: 1
 * Title: sample topic
 * Description: A sample topic description.
 * 1  This is the first turn
 * 2  This is the second turn.
 * ...
 * A blank line separates topics.
 *
 */
public class TopicTextReaderY2 {

  /**
   * Parses a topic text file and produces a list of Topic objects.
   *
   */
  public List<Topic> parseTopicTextFile(String topicFile) throws Exception {
    List<String> lines = Files.readAllLines(Paths.get(topicFile));
    Topic.Builder topicBuilder = Topic.newBuilder();
    List<Topic> topicList = new ArrayList<Topic>();
    int curTopicNumber = 81;
    int curTurn = 0;
    TopicDef.Turn.Builder turnBuilder = TopicDef.Turn.newBuilder();
    for (String line : lines) {
      System.out.println(line);
      String lowercased = line.toLowerCase();
      String[] fields = line.split("\t");
      if (lowercased.startsWith("number:")) {
        if (curTopicNumber > 81) {
          if (curTurn > 1) {
            turnBuilder.setNumber(curTurn);
            topicBuilder.addTurn(turnBuilder.build());
            turnBuilder = TopicDef.Turn.newBuilder();
          }
          Topic topic = topicBuilder.build();
          checkTopic(topic);
          topicList.add(topic);
          topicBuilder = Topic.newBuilder();
          turnBuilder = TopicDef.Turn.newBuilder();
          curTurn = 0;
        }
        String numberString = line.replace("Number:", "").trim();
//        String[] numberStringParts = numberString.split("-");
//        int number = Integer.parseInt(numberString);
//        topicBuilder.setNumber(number);
        topicBuilder.setNumber(curTopicNumber);
        curTopicNumber++;
      } else if (lowercased.startsWith("title:")) {
        String titleString = line.replace("Title:", "").trim();
        topicBuilder.setTitle(titleString);
      } else if (lowercased.startsWith("description:")) {
        String descriptionString = line.replace("Description:", "").trim();
        topicBuilder.setDescription(descriptionString);
      } else if (lowercased.startsWith("turn:")) {
        turnBuilder.setNumber(curTurn);
        if (curTurn > 0) {
          topicBuilder.addTurn(turnBuilder.build());
          turnBuilder = TopicDef.Turn.newBuilder();
        }
        curTurn++;
      } else if (lowercased.startsWith("query turn")) {
        String result = line.replace("Query Turn Dependence:", "").replace("Query Turn dependence:", "").trim();
        if (!result.trim().isEmpty()) {
          String[] split = result.split(",");
          ArrayList<Integer> turnIds = new ArrayList();
          if (split.length > 0) {
            for (String turnString : split) {
              int turnId = Integer.parseInt(turnString.trim());
              turnIds.add(turnId);
            }
            turnBuilder.addAllQueryTurnDependence(turnIds);
          }
        }
    } else if (lowercased.startsWith("result turn")) {
      String result = line.replace("Result Turn Dependence:", "").replace("Result Turn dependence:", "").trim();
      if (!result.trim().isEmpty()) {
        turnBuilder.setResultTurnDependence(Integer.parseInt(result.trim()));
      }
    } else if (lowercased.startsWith("utterance:")) {
        String rawUtterance = line.replace("Utterance:", "").trim();
        turnBuilder.setRawUtterance(rawUtterance);
      }  else if (lowercased.startsWith("resolved:")) {
      String resolvedUtterance = line.replace("Resolved:", "").trim();
      turnBuilder.setManualRewrittenUtterance(resolvedUtterance);
      }  else if (lowercased.startsWith("result")) {
        String result = line.replace("Result(s):", "").replace("Result:", "").replace("Results:", "").trim();
        turnBuilder.setCanonicalResultId(result);
      }
       else {
        if (!line.trim().isEmpty()) {
          System.out.println("Ignoring other field: " + line);
        }
        //throw new Exception("Invalid text file format on line: " + line);
      }
    }
    turnBuilder.setNumber(curTurn);
    topicBuilder.addTurn(turnBuilder.build());

    Topic topic = topicBuilder.build();
    checkTopic(topic);
    topicList.add(topic);
    return topicList;
  }

  private void checkTopic(Topic topic) throws Exception {
    if (topic == null) {
      throw new IllegalArgumentException("topic is null");
    }
    if (topic.getTurnList().isEmpty()) {
      throw new IllegalArgumentException("topic has no turns, it must have at least one turn.");
    }

    int curIdx = 1;
    for (TopicDef.Turn turn : topic.getTurnList()) {
      if (turn.getNumber() != curIdx) {
        throw new IllegalArgumentException("topic turns are out of order." + turn.toString());
      }
      curIdx++;
    }
  }


  public static void main(String[] args) throws Exception{
    System.out.println("Loading topics.");
    TopicTextReaderY2 reader = new TopicTextReaderY2();
    List<Topic> topicList = reader.parseTopicTextFile(args[0]);
    // Simply print out the topics loaded.
    System.out.println("Number of topics:" + topicList.size());
    for (Topic topic : topicList) {
      System.out.println(topic.toString());
    }
  }
}