import os
import sys
import copy

import pytest

from main import get_service_stub, load_turn_lookup_set, load_run_file
from main import validate_turn, validate_run, validate

def test_get_service_stub(grpc_server_test):
    assert(get_service_stub() is not None)

def test_load_turn_lookup_set(turns_lookup_path):
    turn_lookup_set = load_turn_lookup_set(turns_lookup_path)
    assert(len(turn_lookup_set) == 205)

def test_load_invalid_turn_lookup_set(tmp_path):
    tmp_file = tmp_path / 'invalid.json'
    json_str = '{"foo": "bar"}'

    with open(tmp_file, 'w') as tf:
        tf.write(json_str)

    with pytest.raises(AssertionError):
        _ = load_turn_lookup_set(tmp_file)

def test_load_missing_turn_lookup_set():
    with pytest.raises(Exception):
        _ = load_turn_lookup_set('foobar')

def test_load_run_file(run_file_path):
    load_run_file(run_file_path)

def test_validate_invalid_run_file(tmp_path):
    tmp_file = tmp_path / 'invalid.json'
    json_str = '{"foo": "bar"}'
    
    with open(tmp_file, 'w') as tf:
        tf.write(json_str)

    with pytest.raises(Exception):
        _ = load_run_file(tmp_file)

def test_validate_missing_run_file():
    with pytest.raises(OSError):
        _ = load_run_file('foobar')

def test_validate_turn(turns_lookup_path, run_file_path, grpc_stub_test, sample_turn):
    turn_lookup_set = load_turn_lookup_set(turns_lookup_path)
    warnings, service_errors = validate_turn(sample_turn, turn_lookup_set, grpc_stub_test)
    assert(warnings == 4) # due to small database being used
    assert(service_errors == 0)

def test_validate_run(turns_lookup_path, run_file_path, grpc_stub_test, default_validate_args):
    args = default_validate_args
    turn_lookup_set = load_turn_lookup_set(turns_lookup_path)
    run = load_run_file(run_file_path)
    assert(len(run.turns) == 205)
    
    turns_validated, service_errors, total_warnings = validate_run(run, turn_lookup_set, grpc_stub_test, args.max_warnings, args.strict)
    assert(turns_validated == 9)
    assert(service_errors == 0)
    assert(total_warnings == 28)

def test_validate_run_strict(turns_lookup_path, run_file_path, grpc_stub_test, default_validate_args):
    args = default_validate_args
    args.strict = True
    turn_lookup_set = load_turn_lookup_set(turns_lookup_path)
    run = load_run_file(run_file_path)
    assert(len(run.turns) == 205)
    
    turns_validated, service_errors, total_warnings = validate_run(run, turn_lookup_set, grpc_stub_test, args.max_warnings, args.strict)
    assert(turns_validated == 9)
    assert(service_errors == 0)
    assert(total_warnings == 28)

def test_validate_run_no_service(turns_lookup_path, run_file_path, default_validate_args):
    args = default_validate_args
    turn_lookup_set = load_turn_lookup_set(turns_lookup_path)
    run = load_run_file(run_file_path)
    assert(len(run.turns) == 205)
    
    turns_validated, service_errors, total_warnings = validate_run(run, turn_lookup_set, None, args.max_warnings, args.strict)
    assert(turns_validated == 205)
    assert(service_errors == 0)
    assert(total_warnings == 0)

@pytest.mark.slow
def test_validate(default_validate_args, grpc_server_full):
    args = default_validate_args

    turns_validated, service_errors, total_warnings = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)
    assert(turns_validated == 205)
    assert(service_errors == 0)
    assert(total_warnings == 1) # seems to be 1 invalid ID in the sample_runs.json file?

@pytest.mark.slow
def test_validate_no_service(default_validate_args, grpc_server_full):
    args = default_validate_args

    # terminate the service
    grpc_server_full.stop(None)

    turns_validated, service_errors, total_warnings = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)
    assert(turns_validated == 205)
    assert(service_errors == 205)
    assert(total_warnings == 0) 

@pytest.mark.slow
def test_validate_no_service_skip_validation(default_validate_args, grpc_server_full):
    args = default_validate_args
    args.skip_passage_validation = True

    # terminate the service
    grpc_server_full.stop(None)

    turns_validated, service_errors, total_warnings = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)
    assert(turns_validated == 205)
    assert(service_errors == 0)
    assert(total_warnings == 0) 

@pytest.mark.slow
def test_validate_no_service_strict(default_validate_args, grpc_server_full):
    args = default_validate_args
    args.strict = True

    # terminate the service
    grpc_server_full.stop(None)

    turns_validated, service_errors, total_warnings = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)
    assert(turns_validated == 1)
    assert(service_errors == 1)
    assert(total_warnings == 0) 

def test_validate_empty(default_validate_args):
    args = default_validate_args
    args.path_to_run_file = 'foobar'
    with pytest.raises(FileNotFoundError):
        _, _, _ = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)

def test_validate_small(default_validate_args, grpc_server_test):
    args = default_validate_args
    
    # this should abort after generating enough warnings, since the smaller database won't match most of the IDs
    turns_validated, service_errors, total_warnings = validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)

    assert(turns_validated == 9)
    assert(service_errors == 0)
    assert(total_warnings == 28)
