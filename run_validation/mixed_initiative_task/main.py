import os
import argparse
import json
import logging
import sys

from pathlib import PurePath

from compiled_protobufs.mi_run_pb2 import CasTMiRun, Turn
from google.protobuf.json_format import ParseDict

EXPECTED_TURNS = 205
EXPECTED_POOL_SIZE = 4497

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def load_turn_ids(turn_ids_path: str) -> set:
    if not os.path.exists(turn_ids_path):
        logger.error(f'Unable to open turn IDs file: {turn_ids_path}')
        sys.exit(255)

    turn_lookup_set = set()

    # collect all turn ids
    with open(turn_ids_path) as turn_ids_file:
        try:
            turn_ids_dict = json.load(turn_ids_file)
        except json.decoder.JSONDecodeError as jde:
            logger.error(f'JSON error loading turn IDs file: {jde}')
            sys.exit(255)

        for topic, turn_list in turn_ids_dict.items():
            turn_list = [f'{topic}_{turn}' for turn in turn_list]
            for turn in turn_list:
                turn_lookup_set.add(turn)

    # check that topics were loaded correctly
    try:
        assert len(turn_lookup_set) == EXPECTED_TURNS
    except AssertionError:
        logger.error(f'Topics file not loaded correctly (expected {EXPECTED_TURNS} turns, found {len(turn_lookup_set)}')
        sys.exit(255)

    return turn_lookup_set

def load_question_pool(question_pool_path: str) -> dict:
    if not os.path.exists(question_pool_path):
        logger.error(f'Unable to open question pool file: {question_pool_path}')
        sys.exit(255)

    # collect all questions in pool
    question_pool_dict = {}
    with open(question_pool_path) as question_pool_file:
        try:
            question_pool = json.load(question_pool_file)
        except json.decoder.JSONDecodeError as jde:
            logger.error(f'JSON error loading question pool file: {jde}')
            sys.exit(255)

        try:
            for question in question_pool:
                question_pool_dict[question['question_id']] = question['question']
        except KeyError:
            logger.error('Question pool file not loaded correctly (missing JSON keys)')
            sys.exit(255)

    # check that topics were loaded correctly
    try:
        assert len(question_pool_dict) == EXPECTED_POOL_SIZE
    except AssertionError:
        logger.error('Question pool file not loaded correctly (expected {EXPECTED_POOL_SIZE} entries, found {len(question_pool_dict)}')
        sys.exit(255)

    return question_pool_dict

def load_run_file(run_file_path: str) -> CasTMiRun:
    if not os.path.exists(run_file_path):
        logger.error(f'Unable to open run file: {run_file_path}')
        sys.exit(255)

    # validate structure
    with open(run_file_path) as run_file:
        try:
            run = json.load(run_file)
            run = ParseDict(run, CasTMiRun())
        except Exception as e:
            # Run file is not in the right format. Exit
            logger.error(e)
            logger.error('Run file not in the right format. Exiting...')
            sys.exit(255)

    # run checks
    if len(run.turns) == 0:
        logger.error('Run file does not have any turns. Exiting...')
        sys.exit(255)

    return run

def validate_turn(turn: Turn, turn_lookup_set: set, question_pool_dict: dict) -> int:
    turn_warnings = 0

    if len(turn.questions) == 0:
        logger.warning(f'Turn {turn.turn_id} contains no questions!')
        turn_warnings += 1
        return turn_warnings

    if turn.turn_id in turn_lookup_set:
        for index, question in enumerate(turn.questions):
            if not question.question or not question.score:
                logger.warning(f'Turn {turn.turn_id} contains an empty question or question without score in question ranking at index {index}')
                turn_warnings += 1
            if question.question.startswith('Q') and question.question[1:].isdigit():
                # check if question id is valid
                if question.question not in question_pool_dict:
                    logger.warning(f'{question.question} is not valid')
                    turn_warnings += 1
    else:
        logger.warning(f'Turn number {turn.turn_id} is not valid')
        turn_warnings += 1

    return turn_warnings

def validate_run(run_file_path: str, fileroot: str) -> int:
    run_file_name = PurePath(run_file_path).name
    fileHandler = logging.FileHandler(filename=f'{run_file_name}.errlog')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    turn_lookup_set = load_turn_ids(os.path.join(fileroot, 'files/2022_evaluation_topics_turn_ids.json'))

    question_pool_dict = load_question_pool(os.path.join(fileroot, 'files/2022_mixed_initiative_question_pool.json'))

    run = load_run_file(run_file_path)

    warning_count = 0

    # check turns are valid
    for turn in run.turns:
        warning_count += validate_turn(turn, turn_lookup_set, question_pool_dict)

        if warning_count >= 25:
            # too many warnings
            logger.error('Too many Warnings. Exiting..')
            sys.exit(255)

    return warning_count

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='TREC 2022 CAsT mixed initiative task validator',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('task_name')
    ap.add_argument('path_to_run_file')
    ap.add_argument('-f', '--fileroot', help='Location of data files',
                    default='.')
    args = ap.parse_args()

    if args.task_name != 'CAST':
        logger.error(f'Unrecognised task name: {args.task_name}')
        sys.exit(255)

    validate_run(args.path_to_run_file, args.fileroot)
