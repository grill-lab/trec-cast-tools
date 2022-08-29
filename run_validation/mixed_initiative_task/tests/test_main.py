import pytest

from main import load_turn_ids, load_question_pool, load_run_file
from main import validate_turn, validate_run
from main import EXPECTED_POOL_SIZE, EXPECTED_TURNS

def check_sys_exit(pytest_exc, code=255):
    assert(pytest_exc.type == SystemExit)
    assert(pytest_exc.value.code == code)

def test_load_turn_ids(turn_ids_path):
    assert(len(load_turn_ids(turn_ids_path)) == EXPECTED_TURNS)

def test_load_invalid_turn_ids(tmp_path):
    path = tmp_path / 'invalid_turn.json'
    with open(path, 'w') as f:
        f.write('[not valid json]{}!___')

    # loading an invalid JSON file
    with pytest.raises(SystemExit) as pytest_exc:
        load_turn_ids(path)

    check_sys_exit(pytest_exc)

    path = tmp_path / 'missing_turns.json'
    with open(path, 'w') as f:
        f.write('{"132":[], "133":[]}')

    # loading a valid JSON file with unexpected number of turns
    with pytest.raises(SystemExit) as pytest_exc:
        load_turn_ids(path)

    check_sys_exit(pytest_exc)

def test_load_missing_turn_ids(tmp_path):
    with pytest.raises(SystemExit) as pytest_exc:
        load_turn_ids(tmp_path / 'foobar')

    check_sys_exit(pytest_exc)

def test_load_question_pool(question_pool_path):
    assert(len(load_question_pool(question_pool_path)) == EXPECTED_POOL_SIZE)

def test_load_invalid_question_pool(tmp_path):
    path = tmp_path / 'invalid_pool.json'
    with open(path, 'w') as f:
        f.write('[not valid json]{}!___')

    with pytest.raises(SystemExit) as pytest_exc:
        load_question_pool(path)

    check_sys_exit(pytest_exc)

    path = tmp_path / 'missing_pool_ids.json'
    with open(path, 'w') as f:
        f.write('[{}, {}]')

    with pytest.raises(SystemExit) as pytest_exc:
        load_question_pool(path)

    check_sys_exit(pytest_exc)

def test_load_missing_question_pool(tmp_path):
    with pytest.raises(SystemExit) as pytest_exc:
        load_question_pool(tmp_path / 'foobar')

    check_sys_exit(pytest_exc)

def test_load_run_file(run_file_path):
    run = load_run_file(run_file_path)
    assert(len(run.turns) == 284)

def test_load_invalid_run_file(tmp_path):
    path = tmp_path / 'invalid_run.json'
    with open(path, 'w') as f:
        f.write('[not valid json]{}!___')

    with pytest.raises(SystemExit) as pytest_exc:
        load_run_file(path)

    check_sys_exit(pytest_exc)

    path = tmp_path / 'missing_turns.json'
    with open(path, 'w') as f:
        f.write('[{}, {}]')

    with pytest.raises(SystemExit) as pytest_exc:
        load_run_file(path)

    check_sys_exit(pytest_exc)

def test_load_missing_run_file(tmp_path):
    with pytest.raises(SystemExit) as pytest_exc:
        load_run_file(tmp_path / 'foobar')

    check_sys_exit(pytest_exc)

def test_validate_turn(sample_turn, turn_lookup_set, question_lookup_dict):
    turn_warnings = validate_turn(sample_turn, turn_lookup_set, question_lookup_dict)

    assert(turn_warnings == 0)

def test_validate_invalid_turn(sample_turn, turn_lookup_set, question_lookup_dict):
    turn_warnings = validate_turn(sample_turn, set(), question_lookup_dict)
    assert(turn_warnings == 1)

    turn_warnings = validate_turn(sample_turn, turn_lookup_set, {})
    assert(turn_warnings == 10)

    del sample_turn.questions[:]
    turn_warnings = validate_turn(sample_turn, turn_lookup_set, {})
    assert(turn_warnings == 1)
