import re
import spacy
nlp = spacy.load("en_core_web_sm")

class RegexPassageChunker:
    def __init__(self, docid, title, text, url):
        self.document = self.sanitize_document(text)
        self.sentences = self.sentence_tokenization()
        self.url = url
        self.title = title
        self.docid = docid
        
    def sentence_tokenization(self):
        '''
        Tokenizes document into sentences using regex.
        '''
        
        return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", self.document)
    
    def create_passages(self, passage_size = 250):
        '''
        Creates passages of roughly 250 words -- most passages are less than 250.
        '''
        passages = []
        content_length = len(self.sentences)
        sentences_word_count = [len(re.findall(r'\w+', sentence)) for sentence in self.sentences]
        
        passage_id = 0
        
        current_idx = 0
        current_passage_word_count = 0
        current_passage = ''
        sub_id = 0
        
        for i in range(content_length):
            if current_passage_word_count >= (passage_size * 0.67):
                passages.append({
                    "body": current_passage,
                    "title": self.title,
                    "id": f"{self.docid}:{sub_id}",
                    "url": self.url
                })
                current_passage = ''
                current_passage_word_count = 0
                
                current_idx = i
                sub_id += 1
            
            current_passage += self.sentences[i] + ' '
            current_passage_word_count += sentences_word_count[i]
        
        current_passage = ' '.join(self.sentences[current_idx:])
        passages.append({
            "body": current_passage,
            "title": self.title,
            "id": f"{self.docid}:{sub_id}",
            "url": self.url
        })
        
        return passages
    
    def sanitize_document(self, doc):
        '''
        - Removes html formatting from text 
        '''
        sanitized = re.compile('<.*?>')
        return re.sub(sanitized, '', doc)

#We might decide to use Spacy. Spacy is more accurate but much slower than regex   
class SpacyPassageChunker:
    def __init__(self, docid, title, text, url):
        self.document = nlp(self.sanitize_document(text))
        self.sentences = []
        self.url = url
        self.title = title
        self.docid = docid
    
    def sentence_tokenization(self):
        self.sentences = list(text.sents)
        #self.sentences = [sent.text for self.sentences.text]
    
    def create_passages(self, passage_size = 250):
        passages = []
        content_length = len(self.sentences)
        sentences_word_count = [len([token for token in sentence]) for sentence in self.sentences]
        
        passage_id = 0
        current_idx = 0
        current__passage_word_count = 0
        current_passage = ''
        sub_id = 0
        
        for i in range(content_length):
            if current_passage_word_count >= (passage_size * 0.67):
                passages.append({
                    "body": current_passage,
                    "title": self.title,
                    "id": f"{self.docid}:{sub_id}",
                    "url": self.url
                })
                current_passage = ''
                current_passage_word_count = 0
                
                current_idx = i
                sub_id += 1
            
            current_passage += self.sentences[i].text + ' '
            current_passage_word_count += sentences_word_count[i]
        
        current_passage = ' '.join(self.sentences[current_idx:])
        passages.append({
            "body": current_passage,
            "title": self.title,
            "id": f"{self.docid}:{sub_id}",
            "url": self.url
        })
        
        return passages
        
        
    def sanitize_document(doc):
        """
        - Removes html formatting from text
        
        Parameters
        ----------
        doc : str
            The piece of text to be sanitized
        
        Returns
        -------
        doc : str
            input doc but without html tags 
        """
        
        sanitized = re.compile('<.*?>')
        return re.sub(sanitized, '', doc)
        
        