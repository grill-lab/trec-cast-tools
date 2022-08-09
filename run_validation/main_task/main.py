import sys
import json
import csv
from pathlib import Path, PurePath
from google.protobuf.json_format import Parse, ParseDict

from compiled_protobufs.run_pb2 import CAsTRun
import logging
import hashlib


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

# collect passge ids and hashes
with open("files/all_hashes.csv") as passage_hashes_file:
    passage_lookup_dict = {}
    passage_hashes_reader = csv.reader(passage_hashes_file)
    for row in passage_hashes_reader:
        passage_lookup_dict[row[0]] = row[1]

# validate structure
with open(sys.argv[2]) as run_file:
    try:
        run = json.load(run_file)
        run = ParseDict(run, CAsTRun())
    except Exception as e:
        # Run file is not in the right format. Exit
        logger.error(e)
        sys.exit(255)

for turn in run.turns:
    # check turns are valid
    if warning_count >= 25:
        # too many warnings
        sys.exit(255)
    if turn.turn_id in turn_lookup_set:
        # check that responses are valid
        for response in turn.responses:
            if not response.text:
                logger.warning(f"{turn.turn_id} response text is missing")
                warning_count += 1
            for provenance in response.provenance:
                if provenance.id in passage_lookup_dict:
                    # check passage text
                    passage_text = provenance.text
                    if passage_text.startswith("\n") and passage_text.endswith("\n"):
                        passage_text = passage_text.strip()
                    # check hash
                    md5_hash = hashlib.md5(passage_text.encode())
                    try:
                        assert md5_hash.hexdigest() == passage_lookup_dict[provenance.id]
                    except Exception as e:
                        logger.warning(f"Passage text for Passage {provenance.id} does not match master")
                        print(md5_hash.hexdigest())
                        warning_count += 1

                else:
                    logger.warning(f"{provenance.id} is not a valid passage id")
                    warning_count += 1
    else:
        logger.warning(f"{turn.turn_id} is not valid")
        warning_count += 1


