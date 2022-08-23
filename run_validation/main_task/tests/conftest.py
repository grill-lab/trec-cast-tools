import os

import pytest

from passage_id_db import PassageIDDatabase

# this file just contains the first 10k lines of all_hashes.csv
SAMPLE_HASHES_PATH = os.path.join(os.path.dirname(__file__), 'sample_hashes.csv')

@pytest.fixture
def sample_database(tmp_path):
    hdb = PassageIDDatabase(tmp_path / 'temp.sqlite3')
    hdb.open()
    hdb.populate(SAMPLE_HASHES_PATH, 5000, 5000)
    yield hdb
    hdb.close()
