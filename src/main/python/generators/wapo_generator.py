import tarfile
from tqdm import tqdm
import json
import re

from .abstract_generator import AbstractGenerator
from typing import Dict, List


class WaPoGenerator(AbstractGenerator):

    def __init__(self, collection_path, duplicates_path, batch_size: int = 100000) -> None:
        super().__init__(collection_path, duplicates_path, batch_size)
        self.CLEANR = re.compile('<.*?>')
        

    def generate_documents(self) -> List[Dict]:

        document_batch = []

        with tarfile.open(self.collection_path) as wapo_zip:

            print("--Loading WaPo collection (might take a minute or two)--")
            wapo_collection = wapo_zip.extractfile(
                "WashingtonPost.v4/data/TREC_Washington_Post_collection.v4.jl"
            )
            print("--WaPo loaded--")

            for line in tqdm(wapo_collection, total=728626):
                raw_document = json.loads(line)
                doc_id = 'WAPO_' + raw_document['id']
                if doc_id in self.blacklist_ids:
                    continue
                else:
                    # address url issues
                    if "washingtonpost" not in raw_document["article_url"]:
                        raw_document["article_url"] = "https://www.washingtonpost.com" + \
                            raw_document['article_url']

                    # account for empty titles
                    raw_document['title'] = raw_document.get(
                        'title', 'No Title')
                    
                    # extract body
                    document_body = ''
                    try:
                        if raw_document.get('contents') and len(raw_document['contents']) > 0:
                            for item in raw_document['contents']:
                                if item.get('subtype') == 'paragraph':
                                    document_body += ' ' + item['content']
                    except:
                        continue # content to extract
                    document_body = self.__cleanhtml(document_body)

                    parsed_document = {
                        "id": doc_id,
                        "url": raw_document['article_url'],
                        "title": raw_document['title'],
                        "contents": document_body.replace("\n", " ").strip()
                    }
                    document_batch.append(parsed_document)

                if len(document_batch) == self.batch_size:
                    yield document_batch
                    document_batch = []

        if len(document_batch) > 0:
            yield document_batch


    def __cleanhtml(self, text):
        cleantext = re.sub(self.CLEANR, '', text)
        return cleantext
