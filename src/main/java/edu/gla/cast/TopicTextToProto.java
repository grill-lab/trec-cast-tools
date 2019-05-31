package edu.gla.cast

import java.io.File
import java.io.FileWriter
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Paths
import java.util.ArrayList

import cast.topics.TopicDef.*
import com.google.protobuf.util.JsonFormat

/**
 * Read in a topic text file and create a protocol buffer / json file output.
 *
 */
class TopicTextToProto {


    /**
     * Parses a topic text file and produces a list of Topic objects.
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
    @Throws(Exception::class)
    fun parseTopicTextFile(topicFile: String): List<Topic> {
        val lines = Files.readAllLines(Paths.get(topicFile))
        val topic = Topic.newBuilder()
        val topicList = ArrayList<Topic>()
        for (line in lines) {
            println(line)
            val lowercased = line.toLowerCase()
            val fields = lowercased.split("/t".toRegex()).dropLastWhile({ it.isEmpty() }).toTypedArray()
            if (lowercased.startsWith("number:")) {
                val numberString = line.replace("Number:", "").trim({ it <= ' ' })
                val number = Integer.parseInt(numberString)
                topic.number = number
            } else if (lowercased.startsWith("title:")) {
                val titleString = line.replace("Title:", "").trim({ it <= ' ' })
                topic.title = titleString
            } else if (lowercased.startsWith("description:")) {
                val descriptionString = line.replace("Description:", "").trim({ it <= ' ' })
                topic.description = descriptionString
            } else if (lowercased.isEmpty()) {
                topicList.add(topic.build())
            } else if (fields.size == 2) {
                // An individual turn in the topic.
                val turnNumber = Integer.parseInt(fields[0])
                val utterance = fields[1]
                val turn = Turn.newBuilder()
                turn.number = turnNumber
                turn.rawUtterance = utterance
                topic.addTurn(turn.build())
            } else {
                throw Exception("Invalid text file format on line: $line")
            }
        }
        topicList.add(topic.build())
        return topicList
    }

    @Throws(IOException::class)
    fun writeTopicToFile(topics: List<Topic>, outputFile: File) {
        val writer = FileWriter(outputFile)
        try {
            for (topic in topics) {
                val jsonString = JsonFormat.printer()
                        .preservingProtoFieldNames()
                        .includingDefaultValueFields()
                        .print(topic)
                println("Writing json string: $jsonString")
                writer.write(jsonString)
            }
        } finally {
            writer.close()
        }

    }

    companion object {

        @Throws(Exception::class)
        @JvmStatic
        fun main(args: Array<String>) {
            println("Loading topics.")
            val topicTextToProto = TopicTextToProto()
            val topicList = topicTextToProto.parseTopicTextFile(args[0])
            println("Number of topics:" + topicList.size)

        }
    }
}
