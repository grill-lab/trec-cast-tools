import sys
sys.path.append("./compiled_protobufs")
import argparse

from concurrent import futures

import grpc

from compiled_protobufs.passage_validator_pb2_grpc import \
    add_PassageValidatorServicer_to_server
from passage_validator import PassageValidator as PassageValidatorServicer

# for all_hashes.csv
EXPECTED_ID_COUNT = 106400940

def serve(db_path, expected_rows):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PassageValidatorServicer_to_server(PassageValidatorServicer(db_path, expected_rows), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('db_path', type=str, help='SQLite database path', default='./files/all_hashes.sqlite3')
    parser.add_argument('expected_rows', type=int, help='Expected number of rows in database (0 to skip checking)', default=EXPECTED_ID_COUNT)
    args = parser.parse_args()
    serve(args.db_path, args.expected_rows)
