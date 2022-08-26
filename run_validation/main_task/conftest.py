import os
import sys
import csv
import logging
from types import SimpleNamespace
from concurrent import futures

import pytest
import grpc

test_root = os.path.dirname(__file__)
sys.path.append(os.path.join(test_root, 'compiled_protobufs'))

from passage_validator import PassageValidator as PassageValidatorServicer
from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorStub
from compiled_protobufs.passage_validator_pb2_grpc import add_PassageValidatorServicer_to_server
from passage_id_db import PassageIDDatabase
from passage_validator_servicer import EXPECTED_ID_COUNT
from main import load_run_file, get_service_stub

# see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def pytest_addoption(parser):
    parser.addoption('--runslow', action='store_true', default=False, help='Run slow tests')

def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: mark test as slow to run')

def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)

# this file just contains the first 10k lines of all_hashes.csv
SAMPLE_HASHES_PATH = os.path.join(test_root, 'tests', 'sample_hashes.csv')
# database version of the same file
SAMPLE_DB_PATH = os.path.join(test_root, 'tests', 'sample_hashes.sqlite3')
SAMPLE_DB_COUNT = 10000

FULL_DB_PATH = os.path.join(test_root, 'files', 'all_hashes.sqlite3')

TURNS_LOOKUP_PATH = os.path.join(test_root, 'files', '2022_evaluation_topics_turn_ids.json')

RUN_FILE_PATH = os.path.join(os.path.dirname(test_root), 'sample_runs', 'sample_run.json')

@pytest.fixture
def sample_database(tmp_path):
    # create a temporary SQLite database from the contents of sample_hashes.csv
    hdb = PassageIDDatabase(tmp_path / 'temp.sqlite3')
    hdb.open()
    hdb.populate(SAMPLE_HASHES_PATH, 5000, 1)
    yield hdb
    hdb.close()

@pytest.fixture
def sample_ids():
    # return a list of the valid IDs from sample_hashes.csv
    ids = []
    with open(SAMPLE_HASHES_PATH, 'r') as f:
        rdr = csv.reader(f)
        ids = [line[0] for line in rdr]
    yield ids

@pytest.fixture
def turns_lookup_path():
    yield TURNS_LOOKUP_PATH

@pytest.fixture
def run_file_path():
    yield RUN_FILE_PATH

@pytest.fixture
def default_validate_args():
    yield SimpleNamespace(
        path_to_run_file=RUN_FILE_PATH,
        task_name='CAST',
        max_warnings=25,
        skip_passage_validation=False,
        fileroot=test_root,
        strict=False,
    )

@pytest.fixture
def sample_turn(run_file_path):
    run = load_run_file(run_file_path)
    turn = run.turns[0]
    yield turn

@pytest.fixture
def test_logger(scope='module'):
    logger = logging.Logger('test_logger')
    yield logger

@pytest.fixture
def servicer_params_full():
    yield (FULL_DB_PATH, EXPECTED_ID_COUNT)

@pytest.fixture
def servicer_params_test():
    yield (SAMPLE_DB_PATH, SAMPLE_DB_COUNT)

@pytest.fixture
def grpc_stub_test(grpc_server_test):
    yield get_service_stub()

@pytest.fixture
def grpc_stub_full(grpc_server_full):
    yield get_service_stub()

@pytest.fixture
def grpc_server_test(servicer_params_test):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PassageValidatorServicer_to_server(PassageValidatorServicer(*servicer_params_test), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    yield server

    server.stop(None)

@pytest.fixture
def grpc_server_full(servicer_params_full):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PassageValidatorServicer_to_server(PassageValidatorServicer(*servicer_params_full), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    yield server

    server.stop(None)
