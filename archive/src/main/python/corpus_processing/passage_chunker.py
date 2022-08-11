import re
import spacy
nlp = spacy.load("en_core_web_sm", exclude=["parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"]) #->senter
nlp.enable_pipe("senter")

print(nlp.pipe_names)


class SpacyPassageChunker:
    def __init__(self):
        self.document = None
        self.sentences = None

    
    def sentence_tokenization(self, document):
        self.document = nlp(self.sanitize_document(document))
        self.sentences = list(self.document.sents)

    
    def create_passages(self, passage_size = 250):

        passages = []
        content_length = len(self.sentences)
        sentences_word_count = [len([token for token in sentence]) for sentence in self.sentences]
        
        current_idx = 0
        current_passage_word_count = 0
        current_passage = ''
        sub_id = 0
        
        for i in range(content_length):
            if current_passage_word_count >= (passage_size * 0.67):
                passages.append({
                    "body": current_passage,
                    "id": sub_id
                })
                current_passage = ''
                current_passage_word_count = 0
                
                current_idx = i
                sub_id += 1
            
            current_passage += self.sentences[i].text + ' '
            current_passage_word_count += sentences_word_count[i]

        
        current_passage = ' '.join(sentence.text for sentence in self.sentences[current_idx:])
        passages.append({
            "body": current_passage,
            "id": sub_id
        })
        
        return passages
        
        
    def sanitize_document(self, doc):
        
        sanitized = re.compile('<.*?>')
        return re.sub(sanitized, '', doc)
        
        