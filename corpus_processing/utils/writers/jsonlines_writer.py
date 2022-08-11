import json
from typing import List

def write_to_jsonlines(file_path: str, document_batch: List):

    with open(file_path, 'w') as jsonlines_file:
        for document in document_batch:
            json.dump(document, jsonlines_file, ensure_ascii=False)
            jsonlines_file.write('\n')