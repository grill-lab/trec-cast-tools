import gzip
import csv
import sys
from tqdm import tqdm

from .abstract_generator import AbstractGenerator
from typing import Dict, List

csv.field_size_limit(sys.maxsize)

class MARCO_v1_Generator(AbstractGenerator):

    def generate_documents(self) -> List[Dict]:
        
        document_batch = []

        with gzip.open(self.collection_path, 'rt') as marco_v1_zip:
            marco_v1_tsv = csv.reader(marco_v1_zip, delimiter="\t")
            for line in tqdm(marco_v1_tsv, total=3213835):
                doc_id, url, title, body = line
                parsed_document = {
                    "id": 'MARCO_' + doc_id,
                    "url": url,
                    "title": title,
                    "contents": body.replace("\n", " ").strip()
                }

                document_batch.append(parsed_document)

                if len(document_batch) == self.batch_size:
                    yield document_batch
                    document_batch = []
        
        if len(document_batch) > 0:
            yield document_batch