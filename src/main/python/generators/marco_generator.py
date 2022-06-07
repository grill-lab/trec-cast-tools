import tarfile
import gzip
import json
from tqdm import tqdm

from .abstract_generator import AbstractGenerator
from typing import Dict, List


class MARCOGenerator(AbstractGenerator):

    def generate_documents(self) -> List[Dict]:

        document_batch = []

        with tarfile.open(self.collection_path) as marco_tar:
            for member in tqdm(marco_tar.getmembers()):
                if not member.isdir():
                    # extract the file object
                    extracted_marco_member = marco_tar.extractfile(member)
                    # open file object with gzip
                    with gzip.open(extracted_marco_member) as member_zip:
                        # load document and add to batch
                        for line in member_zip:
                            raw_document = json.loads(line)
                            doc_id = 'MARCO_' + raw_document['docid']
                            if doc_id in self.blacklist_ids:
                                continue
                            else:
                                parsed_document = {
                                    "id": doc_id,
                                    "url": raw_document['url'],
                                    "title": raw_document['title'],
                                    "contents": raw_document['body'].replace("\n", " ").strip()
                                }

                            document_batch.append(parsed_document)

                            if len(document_batch) == self.batch_size:
                                yield document_batch
                                document_batch = []

        if len(document_batch) > 0:
            yield document_batch
