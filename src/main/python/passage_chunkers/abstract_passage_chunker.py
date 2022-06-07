from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractPassageChunker(ABC):

    @abstractmethod
    def process_batch(self, document_batch, output_dir) -> List[Dict]:
        """
        Generates passages splits for each document in a batch

        Each document in a batch is of the form
        {
            "id" : doc_id,
            "url": '',
            "title" : '',
            "contents" : ''
        }
        """
        pass

    @staticmethod
    def chunk_document(document_sentences, sentences_word_count, passage_size=250) -> List[Dict]:
        """
        Creates the passage chunks for a given document
        """
        passages = []

        current_passage = ''
        current_passage_word_count = 0
        sub_id = 1

        for sentence, word_count in zip(document_sentences, sentences_word_count):
            if word_count >= passage_size:
                if current_passage:
                    passages.extend([{
                        "body": current_passage,
                        "id": sub_id
                    }, {
                        "body": sentence.text,
                        "id": sub_id+1
                    }])

                    sub_id += 2

                else:
                    passages.append({
                        "body": sentence.text,
                        "id": sub_id
                    })

                    sub_id += 1

            elif word_count + current_passage_word_count > passage_size:
                passages.append({
                    "body": current_passage,
                    "id": sub_id
                })

                current_passage = sentence.text
                current_passage_word_count = word_count
                sub_id += 1

            else:
                current_passage += sentence.text + ' '
                current_passage_word_count += word_count

        if current_passage:
            passages.append({
                "body": current_passage,
                "id": sub_id
            })

        return passages
