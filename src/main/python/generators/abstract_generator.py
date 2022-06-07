from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractGenerator(ABC):

    def __init__(self, collection_path, duplicates_path, batch_size: int = 100000) -> None:
        self.collection_path = collection_path
        self.batch_size = batch_size
        self.blacklist_ids = set()

        # update blacklist ids
        with open(duplicates_path) as duplicates_file:
            for id in duplicates_file:
                self.blacklist_ids.add(id.strip())


    @abstractmethod
    def generate_documents() -> List[Dict]:
        """
        Generates a batch_size batch of documents for processing
        """

        pass
