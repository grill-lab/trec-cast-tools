from operator import ge
import spacy
from tqdm import tqdm
from pathlib import Path
import hashlib

from .abstract_passage_chunker import AbstractPassageChunker
from typing import Dict, List

nlp = spacy.load("en_core_web_sm", exclude=[
                 "parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"])
nlp.enable_pipe("senter")
nlp.max_length = 1500000  # for documents that are longer than the spacy character limit


class SpacyPassageChunker(AbstractPassageChunker):

    def process_batch(self, document_batch, output_dir) -> None:

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print("Generating passages for current batch")
        batch_document_texts = [document['contents'] for document in document_batch]
        processed_document_texts = nlp.pipe(batch_document_texts, n_process=-1)

        for index, document in tqdm(enumerate(processed_document_texts), total=len(document_batch)):
            document_sentences = list(document.sents)
            sentences_word_count = [
                len([token for token in sentence])
                for sentence in document_sentences
            ]

            generated_passages = self.chunk_document(document_sentences, sentences_word_count)

            # write out md5 hashes to file for verification
            with open(f"{output_dir}/passage_md5_hashes.csv", "a") as md5_hash_file:
                for passage in generated_passages:
                    md5_hash = hashlib.md5(passage['body'].encode())
                    md5_hash_file.write(f"{document_batch[index]['id']}-{passage['id']},{md5_hash.hexdigest()}\n")

            document_batch[index]['contents'] = generated_passages

        return document_batch 
