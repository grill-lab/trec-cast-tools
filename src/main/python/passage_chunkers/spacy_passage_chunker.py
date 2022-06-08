from operator import ge
import spacy
from tqdm import tqdm

from .abstract_passage_chunker import AbstractPassageChunker
from typing import Dict, List

nlp = spacy.load("en_core_web_sm", exclude=[
                 "parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"])
nlp.enable_pipe("senter")
nlp.max_length = 2000000  # for documents that are longer than the spacy character limit


class SpacyPassageChunker(AbstractPassageChunker):

    def process_batch(self, document_batch) -> None:

        batch_document_texts = [document['contents'] for document in document_batch]
        processed_document_texts = nlp.pipe(batch_document_texts, n_process=1)

        for index, document in tqdm(enumerate(processed_document_texts), total=len(document_batch)):
            document_sentences = list(document.sents)
            sentences_word_count = [
                len([token for token in sentence])
                for sentence in document_sentences
            ]

            generated_passages = self.chunk_document(document_sentences, sentences_word_count)
            document_batch[index]['contents'] = generated_passages

        return document_batch 
