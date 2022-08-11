import sys
import json
import csv
from pathlib import Path, PurePath
from google.protobuf.json_format import Parse, ParseDict

from compiled_protobufs.mi_run_pb2 import CasTMiRun
import logging


num_arguments = len(sys.argv)
if num_arguments != 3:
    sys.exit("Usage: python3 main.py [task_name] [path_to_run_file]")

run_file_name = PurePath(sys.argv[2]).name
logging.basicConfig(filename= f"{run_file_name}.errlog", level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

warning_count = 0

# collect all turn ids
with open("files/2022_evaluation_topics_turn_ids.json") as turn_ids_file:
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

# collect all questions in pool
question_pool_dict = {}
with open("files/2022_mixed_initiative_question_pool.json") as question_pool_file:
    question_pool = json.load(question_pool_file)
    for question in question_pool:
        question_pool_dict[question['question_id']] = question['question']
# check that topics were loaded correctly
try:
    assert len(question_pool_dict) == 4497
except AssertionError:
    print("Topics file not loaded correctly")
    sys.exit(255)

# validate structure
with open(sys.argv[2]) as run_file:
    try:
        run = json.load(run_file)
        run = ParseDict(run, CasTMiRun())
    except Exception as e:
        # Run file is not in the right format. Exit
        logger.error(e)
        logger.error("Run file not in the right format. Exiting...")
        sys.exit(255)

# run checks
if len(run.turns) == 0:
    logger.error("Run file does not have any turns. Exiting...")
    sys.exit(255)

for turn in run.turns:
    # check turns are valid
    if warning_count >= 25:
        # too many warnings
        logger.error("Too many Warnings. Exiting..")
        sys.exit(255)
    if turn.turn_id in turn_lookup_set:
        for index, question in enumerate(turn.questions):
            if not question.question or not question.score:
                logger.warning(f"Turn {turn.turn_id} contains an empty question or question without score in question ranking at index {index}")
                warning_count += 1
            if question.question.startswith("Q") and question.question[1:].isdigit():
                # check if question id is valid
                if question.question not in question_pool_dict:
                    logger.warning(f"{question.question} is not valid")
                    warning_count += 1

    else:
        logger.warning(f"Turn number {turn.turn_id} is not valid")
        warning_count += 1
