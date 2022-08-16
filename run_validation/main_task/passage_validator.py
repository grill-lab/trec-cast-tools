import csv
import sys
from compiled_protobufs.passage_validator_pb2 import PassageValidationRequest, PassageValidationResult, PassageValidation
from compiled_protobufs.passage_validator_pb2_grpc import PassageValidatorServicer

class PassageValidator(PassageValidatorServicer):

    def __init__(self) -> None:
        # collect passge ids and hashes
        with open("./files/all_hashes.csv") as passage_hashes_file:
            self.passage_lookup_dict = {}
            passage_hashes_reader = csv.reader(passage_hashes_file)
            for row in passage_hashes_reader:
                self.passage_lookup_dict[row[0]] = row[1]

        # check that passage ids and hashes were loaded correctly
        try:
            assert len(self.passage_lookup_dict.keys()) == 106400940
        except AssertionError:
            print("Passage Ids and hashes not loaded correctly")
            sys.exit(255)
        
        print("Passage IDs loaded!")

    def validate_passages(self,  passage_validation_request: PassageValidationRequest, 
        context) -> PassageValidationResult:
        """
        Takes in a list of passage ids and checks for membership in passage 
        lookup dictionary
        """
        passage_validation_result = PassageValidationResult()
        for passage_id in passage_validation_request.passage_ids:
            passage_validation = PassageValidation()
            passage_validation.is_valid = passage_id in self.passage_lookup_dict
            passage_validation_result.passage_validations.append(passage_validation)
        
        return passage_validation_result