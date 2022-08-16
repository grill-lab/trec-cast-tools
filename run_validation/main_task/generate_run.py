# Generate trec run file, if all checks pass
from compiled_protobufs.run_pb2 import CastRun
import argparse
from google.protobuf.json_format import Parse, ParseDict
import json
from pathlib import PurePath

ap = argparse.ArgumentParser(description='TREC 2022 CAsT run generator',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('path_to_run_file')
args = ap.parse_args()

# validate structure
with open(args.path_to_run_file) as run_file:
    run = json.load(run_file)
    run = ParseDict(run, CastRun())

run_file_name = PurePath(args.path_to_run_file).name

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