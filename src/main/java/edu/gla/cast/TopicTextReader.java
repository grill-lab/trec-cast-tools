package edu.gla.cast;

import cast.topics.TopicDef;
import cast.topics.TopicDef.Topic;

import java.io.FileInputStream;
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
public class TopicTextReader {

  /**
   * Parses a topic text file and produces a list of Topic objects.
   *
   */
  public List<Topic> parseTopicTextFile(String topicFile) throws Exception {
    List<String> lines = Files.readAllLines(Paths.get(topicFile));
    Topic.Builder topic = Topic.newBuilder();
    List<Topic> topicList = new ArrayList<Topic>();
    for (String line : lines) {
      System.out.println(line);
      String lowercased = line.toLowerCase();
      String[] fields = line.split("\t");
      if (lowercased.startsWith("number:")) {
        String numberString = line.replace("Number:", "").trim();
        int number = Integer.parseInt(numberString);
        topic.setNumber(number);
      } else if (lowercased.startsWith("title:")) {
        String titleString = line.replace("Title:", "").trim();
        topic.setTitle(titleString);
      } else if (lowercased.startsWith("description:")) {
        String descriptionString = line.replace("Description:", "").trim();
        topic.setDescription(descriptionString);
      } else if (lowercased.isEmpty()) {
        topicList.add(topic.build());
        topic = Topic.newBuilder();
      } else if (fields.length == 2) {
        // An individual turn in the topic.
        int turnNumber = Integer.parseInt(fields[0]);
        String utterance = fields[1];
        TopicDef.Turn.Builder turn = TopicDef.Turn.newBuilder();
        turn.setNumber(turnNumber);
        turn.setRawUtterance(utterance);
        topic.addTurn(turn.build());
      } else {
        throw new Exception("Invalid text file format on line: " + line);
      }
    }
    topicList.add(topic.build());
    return topicList;
  }


  public static void main(String[] args) throws Exception{
    System.out.println("Loading topics.");
    TopicTextReader reader = new TopicTextReader();
    List<Topic> topicList = reader.parseTopicTextFile(args[0]);
    // Simply print out the topics loaded.
    System.out.println("Number of topics:" + topicList.size());
    for (Topic topic : topicList) {
      System.out.println(topic.toString());
    }
  }
}