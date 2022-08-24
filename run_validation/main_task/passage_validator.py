import sys

from compiled_protobufs.passage_validator_pb2 import PassageValidationRequest, PassageValidationResult, PassageValidation
from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorServicer

from passage_id_db import PassageIDDatabase

class PassageValidator(PassageValidatorServicer):

    def __init__(self, db_path: str, expected_rows: int) -> None:
        self.db = PassageIDDatabase(db_path)
        if not self.db.open():
            print('Error: failed to open database, service cannot start!')
            sys.exit(255)

        if expected_rows > 0:
            assert(self.db.rowcount == expected_rows)
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
