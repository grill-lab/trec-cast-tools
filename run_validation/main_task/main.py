import sys
import json
import csv
from pathlib import Path, PurePath
from google.protobuf.json_format import Parse, ParseDict

from compiled_protobufs.run_pb2 import CastRun
import logging
import hashlib
import argparse

ap = argparse.ArgumentParser(description='TREC 2022 CAsT main task validator',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('-f', '--fileroot', help='Location of data files',
                default='.')
ap.add_argument('task_name')
ap.add_argument('path_to_run_file')
args = ap.parse_args()

run_file_name = PurePath(args.path_to_run_file).name
logging.basicConfig(filename= f"{run_file_name}.errlog", level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

warning_count = 0

# collect all turn ids
with open(f"{args.fileroot}/files/2022_evaluation_topics_turn_ids.json") as turn_ids_file:
    turn_ids_dict = json.load(turn_ids_file)
    turn_lookup_set = set()
    for topic, turn_list in turn_ids_dict.items():
        turn_list = [f"{topic}_{turn}" for turn in turn_list]
        for turn in turn_list:
            turn_lookup_set.add(turn)

# check that topics were loaded correctly
try:
    assert len(turn_lookup_set) == 205
except AssertionError:
    print("Topics file not loaded correctly")
    sys.exit(255)

# collect passge ids and hashes
with open(f"{args.fileroot}/files/all_hashes.csv") as passage_hashes_file:
    passage_lookup_dict = {}
    passage_hashes_reader = csv.reader(passage_hashes_file)
    for row in passage_hashes_reader:
        passage_lookup_dict[row[0]] = row[1]

# check that passage ids and hashes were loaded correctly
try:
    assert len(passage_lookup_dict.keys()) == 106400940
except AssertionError:
    print("Passage Ids and hashes not loaded correctly")
    sys.exit(255)

# validate structure
with open(args.path_to_run_file) as run_file:
    try:
        run = json.load(run_file)
        run = ParseDict(run, CastRun())
    except Exception as e:
        # Run file is not in the right format. Exit
        logger.error(e)
        logger.error("Run file not in the right format. Exiting...")
        sys.exit(255)

# Run checks and generate run file
if len(run.turns) == 0:
    logger.error("Run file does not have any turns. Exiting...")
    sys.exit(255)

for turn in run.turns:
    if warning_count >= 25:
        # too many warnings
        logger.error("Too many Warnings. Run file will not be generated")
        sys.exit(255)
    # check turns are valid
    if turn.turn_id in turn_lookup_set:
        # check that responses are valid
        provenance_count = 0
        previous_rank = 0
        for response in turn.responses:
            if not response.rank:
                logger.warning(f"Response rank for turn {turn.turn_id} is missing")
                warning_count += 1
            if response.rank <= previous_rank:
                logger.warning(f"Current rank {response.rank} is less than or equal to previous rank {previous_rank}")
                warning_count += 1
            if not response.text:
                logger.warning(f"Response text for turn {turn.turn_id} is missing")
                warning_count += 1
            previous_score = None
            for provenance in response.provenance:
                if previous_score is None:
                    previous_score = provenance.score
                elif previous_score <= provenance.score:
                    previous_score = provenance.score
                elif previous_score < provenance.score:
                    logger.warning(f"{provenance.id} has a greater score than previous passage. Ranking order not correct")
                    warning_count += 1
                if provenance_count > 1000:
                    logger.warning(f"More than 1000 passages retrieved for turn {turn.turn_id}")
                    warning_count += 1
                if provenance.id not in passage_lookup_dict:
                    logger.warning(f"{provenance.id} is not a valid passage id")
                    warning_count += 1
                provenance_count += 1
    else:
        logger.warning(f"Turn number {turn.turn_id} is not valid")
        warning_count += 1

# Generate trec run file, if all checks pass
with open(f"{run_file_name}.run", "w") as run_file:
    for turn in run.turns:
        provenance_list = list()
        provenance_set = set()
        for response in turn.responses:
            for provenance in response.provenance:
                if provenance.id not in provenance_set:
                    # update provenance score
                    provenance.score = (1 / (response.rank+1)) * provenance.score
                    provenance_list.append(provenance)
                    provenance_set.add(provenance.id)
        # sort list
        provenance_list.sort(key=lambda provenance: provenance.score, reverse=True)
        # write to file
        for rank, provenance in enumerate(provenance_list):
            run_file.write(f"{turn.turn_id}\tQ0\t{provenance.id}\t{rank+1}\t{provenance.score}\t{run.run_name}\n")
