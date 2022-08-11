import json
from tqdm import tqdm

from .abstract_generator import AbstractGenerator
from typing import Dict, List


class KILTGenerator(AbstractGenerator):

    def generate_documents(self) -> List[Dict]:
        
        document_batch = []

        with open(self.collection_path) as kilt_collection:
            for line in tqdm(kilt_collection, total=5903530):
                raw_document = json.loads(line)
                # extract the ID and check if it is in blacklist
                doc_id = 'KILT_' + raw_document['wikipedia_id']
                if doc_id in self.blacklist_ids:
                    continue
                else:
                    parsed_document = {
                        "id" : doc_id,
                        "url": raw_document['history']['url'],
                        "title" : raw_document['wikipedia_title'],
                        "contents" : ' '.join(raw_document['text']).replace("\n", " ").strip()

                    }
                    document_batch.append(parsed_document)

                if len(document_batch) == self.batch_size:
                    yield document_batch
                    document_batch = []
        
        if len(document_batch) > 0:
            yield document_batch
