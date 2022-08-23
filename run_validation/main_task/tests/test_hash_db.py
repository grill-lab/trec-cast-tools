import os

from passage_id_db import PassageIDDatabase

TEMP_FILE = 'temp.sqlite3'

def test_create_empty_database(tmp_path):
    path = tmp_path / TEMP_FILE
    if os.path.exists(path):
        os.unlink(path)

    with PassageIDDatabase(path) as hdb:
        assert hdb.open()
        assert os.path.exists(path)

def test_create_sample_database(sample_database):
    assert sample_database.rowcount == 10000

def test_validation_all_valid(sample_database):
    # should all be valid 
    valid_passage_ids = ['KILT_20988915-1', 'KILT_20989341-1', 'KILT_5135300-1']
    results = sample_database.validate(valid_passage_ids)
    assert results == [True for x in valid_passage_ids]

def test_validation_all_invalid(sample_database):
    # expected results is [True, False, False, True]
    valid_passage_ids = ['KILT_20988915-1', 'foo', 'bar', 'KILT_5135300-1']
    results = sample_database.validate(valid_passage_ids)
    assert results == [True, False, False, True]

