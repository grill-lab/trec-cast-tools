import json as json
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
import neuralcoref
import spacy

with open("/media/jeff/Data/treccast/topics/train_topics_v1.0 gold.json") as datafile:
    topics = json.load(datafile)
topicDf = pd.DataFrame(topics)

print(len(topics))

logging.basicConfig(level=logging.INFO)

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

def runSpacy(topic):
    prevTurns = ""
    for turn in topic['turn']:
        prevTurns += " "
        prevTurns += turn['raw_utterance']
        doc = nlp(prevTurns)
        print(prevTurns)

runSpacy(topics[0])