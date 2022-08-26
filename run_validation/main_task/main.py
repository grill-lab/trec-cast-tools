import os
import sys
sys.path.append('./compiled_protobufs')
import argparse
import json
import logging
from pathlib import PurePath

import grpc
from google.protobuf.json_format import ParseDict

from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorStub
from compiled_protobufs.run_pb2 import CastRun, Turn
from utils import check_provenance, validate_passages, check_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def get_service_stub(ip: str = 'localhost', port: int = 8000) -> PassageValidatorStub:
    try:
        passage_validation_channel = grpc.insecure_channel(f'{ip}:{port}')
        passage_validation_client = PassageValidatorStub(passage_validation_channel)
    except grpc.RpcError as rpce:
        logger.error('A gRPC error occurred connecting to the validator service: {rpce.code().name}')
        return None

    return passage_validation_client

def load_turn_lookup_set(turns_path: str) -> dict:
    if not os.path.exists(turns_path):
        logger.error(f'Turns file {turns_path} not found!')
        raise Exception(f'Turns file {turns_path} not found!')

    # collect all turn ids
    with open(turns_path) as turn_ids_file:
        turn_ids_dict = json.load(turn_ids_file)
        turn_lookup_set = set()
        for topic, turn_list in turn_ids_dict.items():
            turn_list = [f'{topic}_{turn}' for turn in turn_list]
            for turn in turn_list:
                turn_lookup_set.add(turn)

    # check that topics were loaded correctly
    try:
        assert len(turn_lookup_set) == 205
    except AssertionError as ae:
        logger.error('Topics file not loaded correctly')
        raise ae

    return turn_lookup_set

def load_run_file(run_file_path: str) -> CastRun:
    # validate structure
    with open(run_file_path, 'r', encoding='utf-8') as run_file:
        try:
            run = json.load(run_file)
            run = ParseDict(run, CastRun())
        except Exception as e:
            logger.error(f'Run file not in the right format ({e})')
            raise Exception(f'Run file not in the right format ({e})')

    return run

def validate_turn(turn: Turn, turn_lookup_set: dict, service_stub: PassageValidatorStub) -> (int, bool):
    warning_count, service_errors = 0, 0

    # check turns are valid
    if turn.turn_id in turn_lookup_set:
        logger.debug(f'Validating turn {turn.turn_id}')

        # check that responses are valid
        provenance_count = 0
        previous_rank = 0

        # will be None if skip_passage_validation was used
        if service_stub is not None:
            try:
                warning_count = validate_passages(service_stub, logger, warning_count, turn)
            except grpc.RpcError as rpce:
                logger.warning(f'A gRPC error occurred when validating passages ({rpce.code().name})')
                service_errors += 1

        # check response and provenance
        for response in turn.responses:
            # check response
            warning_count = check_response(response, logger, warning_count, previous_rank, turn)
            previous_score = None

            # check provenance
            for provenance in response.provenance:
                previous_score, provenance_score, warning_count = check_provenance(
                    previous_score, 
                    provenance, 
                    logger, 
                    turn, 
                    warning_count, 
                    provenance_count
                )
    else:
        logger.warning(f'Turn number {turn.turn_id} is not valid')
        warning_count += 1

    return warning_count, service_errors

def validate_run(run: CastRun, turn_lookup_set: dict, service_stub: PassageValidatorStub, max_warnings: int, strict: bool) -> (int, int, int):
    total_warnings, service_errors = 0, 0
    turns_validated = 0

    for turn in run.turns:
        _warnings, _service_errors = validate_turn(turn, turn_lookup_set, service_stub)
        total_warnings += _warnings
        service_errors += _service_errors
        turns_validated += 1

        if total_warnings > max_warnings:
            logger.error(f'Maximum number of warnings exceeded ({total_warnings} > {max_warnings}), aborting!')
            return turns_validated, service_errors, total_warnings

        if service_errors > 0 and strict:
            logger.error('Validation service errors encountered and strict mode enabled')
            return turns_validated, service_errors, total_warnings

    logger.info(f'Validation completed on {turns_validated}/{len(run.turns)} turns with {total_warnings} warnings, {service_errors} service errors')
    return turns_validated, service_errors, total_warnings

def validate(run_file_path: str, fileroot: str, max_warnings: int, skip_validation: bool, strict: bool) -> (int, int, int):
    run_file_name = PurePath(run_file_path).name
    fileHandler = logging.FileHandler(filename=f'{run_file_name}.errlog')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # only instantiate the gRPC service client if skip_validation is False
    validator_stub = None if skip_validation else get_service_stub()

    if strict and not skip_validation and validator_stub is None:
        logger.error('Failed to set up validation service and strict checking was requested')
        raise Exception('Failed to set up validation service and strict checking was requested')

    turn_lookup_set = load_turn_lookup_set(f'{fileroot}/files/2022_evaluation_topics_turn_ids.json')

    run = load_run_file(run_file_path)
    
    if len(run.turns) == 0:
        logger.warning('Loaded run file has 0 turns, not performing any validation!')
        return len(run.turns)
   
    turns_validated, service_errors, total_warnings = validate_run(run, turn_lookup_set, validator_stub, max_warnings, strict)

    return turns_validated, service_errors, total_warnings

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='TREC 2022 CAsT main task validator',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('task_name')
    ap.add_argument('path_to_run_file')
    ap.add_argument('-f', '--fileroot', help='Location of data files',
                    default='.')
    ap.add_argument('--skip_passage_validation', action='store_true')
    ap.add_argument('-m', '--max_warnings', help='Maximum number of warnings to allow',
                    type=int, default=25)
    ap.add_argument('-s', '--strict', help='Abort if any passage validation service errors occur',
                    action='store_true')
    args = ap.parse_args()

    validate(args.path_to_run_file, args.fileroot, args.max_warnings, args.skip_passage_validation, args.strict)
