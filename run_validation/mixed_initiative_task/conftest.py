import os
import sys

import pytest

test_root = os.path.dirname(__file__)
sys.path.append(os.path.join(test_root, 'compiled_protobufs'))

from main import load_turn_ids, load_question_pool, load_run_file

@pytest.fixture
def test_root_path():
    yield test_root

@pytest.fixture
def turn_ids_path():
    yield os.path.join(test_root, 'files', '2022_evaluation_topics_turn_ids.json')

@pytest.fixture
def question_pool_path():
    yield os.path.join(test_root, 'files', '2022_mixed_initiative_question_pool.json')

@pytest.fixture
def run_file_path():
    yield os.path.join('..', 'sample_runs', 'sample_mi_run.json')

@pytest.fixture
def turn_lookup_set(turn_ids_path):
    yield load_turn_ids(turn_ids_path)

@pytest.fixture
def question_lookup_dict(question_pool_path):
    yield load_question_pool(question_pool_path)

@pytest.fixture
def run_file(run_file_path):
    yield load_run_file(run_file_path)

@pytest.fixture
def sample_run(run_file_path):
    yield load_run_file(run_file_path)

@pytest.fixture
def sample_turn(sample_run):
    yield sample_run.turns[0]
