import sys
sys.path.append('./compiled_protobufs')
import argparse
import json
import logging
from pathlib import PurePath

import grpc
from google.protobuf.json_format import ParseDict

from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorStub
from compiled_protobufs.run_pb2 import CastRun
from utils import *

ap = argparse.ArgumentParser(description='TREC 2022 CAsT main task validator',
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('task_name')
ap.add_argument('path_to_run_file')
ap.add_argument('-f', '--fileroot', help='Location of data files',
                default='.')
ap.add_argument('--skip_passage_validation', action='store_true')
args = ap.parse_args()

run_file_name = PurePath(args.path_to_run_file).name
logging.basicConfig(filename=f'{run_file_name}.errlog', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

warning_count = 0

passage_validation_channel = grpc.insecure_channel('localhost:8000')
passage_validation_client = PassageValidatorStub(passage_validation_channel)

# collect all turn ids
with open(f'{args.fileroot}/files/2022_evaluation_topics_turn_ids.json') as turn_ids_file:
    turn_ids_dict = json.load(turn_ids_file)
    turn_lookup_set = set()
    for topic, turn_list in turn_ids_dict.items():
        turn_list = [f'{topic}_{turn}' for turn in turn_list]
        for turn in turn_list:
            turn_lookup_set.add(turn)

# check that topics were loaded correctly
try:
    assert len(turn_lookup_set) == 205
except AssertionError:
    print('Topics file not loaded correctly')
    sys.exit(255)

# validate structure
with open(args.path_to_run_file) as run_file:
    try:
        run = json.load(run_file)
        run = ParseDict(run, CastRun())
    except Exception as e:
        # Run file is not in the right format. Exit
        logger.error(e)
        logger.error('Run file not in the right format. Exiting...')
        sys.exit(255)

# Run checks and generate run file
if len(run.turns) == 0:
    logger.error('Run file does not have any turns. Exiting...')
    sys.exit(255)

for turn in run.turns:
    if warning_count >= 25:
        # too many warnings
        logger.error('Too many warnings. Exiting...')
        sys.exit(255)
    # check turns are valid
    if turn.turn_id in turn_lookup_set:
        # check that responses are valid
        provenance_count = 0
        previous_rank = 0

        if not args.skip_passage_validation:
            warning_count = validate_passages(passage_validation_client, logger, warning_count, turn)

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
