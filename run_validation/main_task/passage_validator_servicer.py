import grpc
import sys
sys.path.append("./compiled_protobufs")
from concurrent import futures
from passage_validator import PassageValidator as PassageValidatorServicer
from compiled_protobufs.passage_validator_pb2_grpc import add_PassageValidatorServicer_to_server

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PassageValidatorServicer_to_server(PassageValidatorServicer(), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()