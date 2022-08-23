import sys

from compiled_protobufs.passage_validator_pb2 import PassageValidationRequest, PassageValidationResult, PassageValidation
from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorServicer

from hash_db import HashDatabase

EXEPCTED_HASH_COUNT = 106400940

class PassageValidator(PassageValidatorServicer):

    def __init__(self) -> None:
        self.db = HashDatabase('./files/all_hashes.sqlite3')
        if not self.db.open():
            print('Error: failed to open database, service cannot start!')
            sys.exit(255)

        assert(self.db.rowcount == EXEPCTED_HASH_COUNT)
        print('Service ready')

    def validate_passages(self,  passage_validation_request: PassageValidationRequest, 
            context) -> PassageValidationResult:
        """
        Takes in a list of passage ids and checks if they appear in the database
        """
        passage_validation_result = PassageValidationResult()

        # query database with the set of passage IDs and return a list of bools
        # indicate valid/invalid for each ID
        validation_results = self.db.validate(passage_validation_request.passage_ids)

        for result in validation_results:
            passage_validation = PassageValidation()
            passage_validation.is_valid = result
            passage_validation_result.passage_validations.append(passage_validation)

        return passage_validation_result
